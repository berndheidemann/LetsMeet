#!/usr/bin/env node
// Stub-basierter Test für check-schulserver.sh — ohne reale Datenbank, ohne
// echtes Node-/App-Verzeichnis. Ein Fake-"node" protokolliert argv, env und
// cwd in eine JSON-Datei und liefert einen steuerbaren Exitcode.
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, mkdirSync, writeFileSync, chmodSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const SCRIPT = fileURLToPath(new URL("./check-schulserver.sh", import.meta.url));

function makeFixture() {
  const root = mkdtempSync(join(tmpdir(), "check-schulserver-"));
  const shared = join(root, "shared");
  mkdirSync(join(shared, "env", "bin"), { recursive: true });
  mkdirSync(join(shared, "app"), { recursive: true });
  const outFile = join(root, "out.json");
  const nodeStub = `#!/bin/bash
node -e '
const fs = require("fs");
fs.writeFileSync(process.env.OUT_FILE, JSON.stringify({
  argv: process.argv.slice(1),
  cwd: process.cwd(),
  env: {
    PGHOST: process.env.PGHOST,
    PGPORT: process.env.PGPORT,
    PGDATABASE: process.env.PGDATABASE,
    PGUSER: process.env.PGUSER,
    PGPASSWORD: process.env.PGPASSWORD,
    CONTRACT_VERSION: process.env.CONTRACT_VERSION,
    CHECK_HISTORY_PATH: process.env.CHECK_HISTORY_PATH,
  },
}));
' "$@"
exit "\${STUB_EXIT_CODE:-0}"
`;
  const nodeBin = join(shared, "env", "bin", "node");
  writeFileSync(nodeBin, nodeStub);
  chmodSync(nodeBin, 0o755);
  return { root, shared, outFile };
}

function run(fixture, args, extraEnv = {}) {
  const home = join(fixture.root, "home");
  mkdirSync(home, { recursive: true });
  const result = spawnSync("bash", [SCRIPT, ...args], {
    env: {
      PATH: process.env.PATH,
      HOME: home,
      LETSMEET_SHARED: fixture.shared,
      OUT_FILE: fixture.outFile,
      ...extraEnv,
    },
    encoding: "utf8",
  });
  return result;
}

function readOut(fixture) {
  return JSON.parse(readFileSync(fixture.outFile, "utf8"));
}

let failures = 0;
function test(name, fn) {
  const fixture = makeFixture();
  try {
    fn(fixture);
    console.log(`ok - ${name}`);
  } catch (error) {
    failures += 1;
    console.error(`FAIL - ${name}`);
    console.error(error);
  } finally {
    rmSync(fixture.root, { recursive: true, force: true });
  }
}

test("forwards version, cwd and default env to the node CLI", (fixture) => {
  const result = run(fixture, ["V1"]);
  assert.equal(result.status, 0, result.stderr);
  const out = readOut(fixture);
  assert.equal(out.cwd, join(fixture.shared, "app"));
  assert.deepEqual(out.argv, ["server/dist/cli.js"]);
  assert.equal(out.env.CONTRACT_VERSION, "V1");
  assert.equal(out.env.PGHOST, "127.0.0.1");
  assert.equal(out.env.PGPORT, "5432");
  assert.equal(out.env.PGDATABASE, "lf8_lets_meet_db");
  assert.equal(out.env.PGUSER, "user");
  assert.equal(out.env.PGPASSWORD, "secret");
});

test("forwards --snapshot-out with an absolute path containing spaces and special characters", (fixture) => {
  const snapshotPath = join(fixture.root, "home", "v3 snapshot (Ä)!.json");
  const result = run(fixture, ["V3", "--snapshot-out", snapshotPath]);
  assert.equal(result.status, 0, result.stderr);
  const out = readOut(fixture);
  assert.deepEqual(out.argv, ["server/dist/cli.js", "--snapshot-out", snapshotPath]);
  assert.equal(out.env.CONTRACT_VERSION, "V3");
});

test("forwards --snapshot-compare unchanged", (fixture) => {
  const snapshotPath = join(fixture.root, "home", "snap.json");
  const result = run(fixture, ["V3", "--snapshot-compare", snapshotPath]);
  assert.equal(result.status, 0, result.stderr);
  const out = readOut(fixture);
  assert.deepEqual(out.argv, ["server/dist/cli.js", "--snapshot-compare", snapshotPath]);
});

test("honors LETSMEET_PG_PORT, LETSMEET_NODE and CHECK_HISTORY_PATH overrides", (fixture) => {
  const historyPath = join(fixture.root, "custom-history.jsonl");
  const customNode = join(fixture.root, "custom node (Ä)");
  mkdirSync(join(customNode, "bin"), { recursive: true });
  const stub = readFileSync(join(fixture.shared, "env", "bin", "node"));
  writeFileSync(join(customNode, "bin", "node"), stub, { mode: 0o755 });
  rmSync(join(fixture.shared, "env"), { recursive: true });
  const result = run(fixture, ["V2"], {
    LETSMEET_PG_PORT: "55432",
    LETSMEET_NODE: customNode,
    CHECK_HISTORY_PATH: historyPath,
  });
  assert.equal(result.status, 0, result.stderr);
  const out = readOut(fixture);
  assert.equal(out.env.PGPORT, "55432");
  assert.equal(out.env.CHECK_HISTORY_PATH, historyPath);
});

test("propagates failed checks and technical exit codes unchanged", (fixture) => {
  for (const code of [1, 2]) {
    const result = run(fixture, ["V1"], { STUB_EXIT_CODE: String(code) });
    assert.equal(result.status, code);
  }
});

test("uses LETSMEET_HOME for the history path", (fixture) => {
  const home = join(fixture.root, "custom home");
  const result = run(fixture, ["V2"], { LETSMEET_HOME: home });
  assert.equal(result.status, 0, result.stderr);
  assert.equal(readOut(fixture).env.CHECK_HISTORY_PATH, join(home, "data", "check-history.jsonl"));
});

test("rejects an unknown version instead of silently selecting V1", (fixture) => {
  const result = run(fixture, ["v3"]);
  assert.equal(result.status, 2);
  assert.match(result.stderr, /Unbekannte Version/);
});

test("fails fast with exit code 2 when no version is given", (fixture) => {
  const result = run(fixture, []);
  assert.equal(result.status, 2);
  assert.match(result.stderr, /Version angeben/);
});

test("fails fast with exit code 2 when node is not found", (fixture) => {
  const result = run(fixture, ["V1"], { LETSMEET_NODE: join(fixture.root, "missing") });
  assert.equal(result.status, 2);
  assert.match(result.stderr, /Node nicht gefunden/);
});

test("fails fast with exit code 2 when the app directory is missing", (fixture) => {
  rmSync(join(fixture.shared, "app"), { recursive: true, force: true });
  const result = run(fixture, ["V1"]);
  assert.equal(result.status, 2);
  assert.match(result.stderr, /App-Verzeichnis nicht gefunden/);
});

if (failures > 0) {
  console.error(`${failures} Test(s) fehlgeschlagen.`);
  process.exit(1);
}
console.log("Alle Tests bestanden.");
