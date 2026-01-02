#!/usr/bin/env node
const { parseCommand, runCommands } = require('..');
const { execSync } = require('child_process');

const args = process.argv.slice(2);
if (args.length === 0) {
  console.error('Usage: mcp-k8s "<natural language command>" [--run]');
  process.exit(2);
}

const text = args[0];
const runFlag = args.includes('--run');
const parsed = parseCommand(text);
console.log('Intent:', parsed.intent);
console.log('Note:', parsed.note);
console.log('Suggested kubectl commands:');
parsed.kubectl.forEach(c => console.log('  ', c));

if (runFlag) {
  if (process.env.ALLOW_KUBECTL !== '1') {
    console.error('Execution disabled. Set ALLOW_KUBECTL=1 to enable running kubectl.');
    process.exit(1);
  }
  for (const c of parsed.kubectl) {
    console.log('\n$ ', c);
    try {
      const out = execSync(c, { stdio: 'inherit' });
    } catch (e) {
      console.error('Command failed:', e.message);
      process.exit(1);
    }
  }
}
