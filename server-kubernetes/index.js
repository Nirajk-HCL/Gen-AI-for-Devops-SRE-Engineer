const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');

function parseCommand(nl) {
  const text = (nl || '').toLowerCase();
  const res = { intent: null, kubectl: [], note: '' };

  if (text.includes('show') && text.includes('pods')) {
    // Show pods in a namespace
    const nsMatch = text.match(/namespace\s+(\w+)/);
    const ns = nsMatch ? nsMatch[1] : 'default';
    res.intent = 'show-pods';
    res.kubectl.push(`kubectl get pods -n ${ns} -o wide`);
    res.note = `Listing pods in namespace '${ns}'`;
    return res;
  }

  const scaleMatch = text.match(/scale .*deployment\s+(\S+)\s+to\s+(\d+)\s+replicas/);
  if (scaleMatch) {
    const deploy = scaleMatch[1];
    const replicas = scaleMatch[2];
    const nsMatch = text.match(/namespace\s+(\w+)/);
    const ns = nsMatch ? nsMatch[1] : 'default';
    res.intent = 'scale-deployment';
    res.kubectl.push(`kubectl scale deployment/${deploy} --replicas=${replicas} -n ${ns}`);
    res.kubectl.push(`kubectl rollout status deployment/${deploy} -n ${ns} --timeout=120s`);
    res.note = `Scale deployment '${deploy}' to ${replicas} replicas in '${ns}' and verify rollout`;
    return res;
  }

  if (text.includes('investigate') && text.includes('crash') || text.includes('crashing')) {
    // Investigate a service crashing: gather pods, logs, and events
    const svcMatch = text.match(/service\s+(\S+)/);
    const svc = svcMatch ? svcMatch[1] : null;
    const nsMatch = text.match(/namespace\s+(\w+)/);
    const ns = nsMatch ? nsMatch[1] : 'default';
    res.intent = 'investigate-crash';
    if (svc) {
      // find pods for the service (by label app=svc)
      res.kubectl.push(`kubectl get pods -l app=${svc} -n ${ns} -o wide`);
      res.kubectl.push(`kubectl logs -l app=${svc} -n ${ns} --tail=200`);
      res.kubectl.push(`kubectl describe pods -l app=${svc} -n ${ns}`);
    } else {
      // generic investigation
      res.kubectl.push(`kubectl get pods -n ${ns} -o wide`);
      res.kubectl.push(`kubectl get events -n ${ns} --sort-by=.metadata.creationTimestamp`);
      res.kubectl.push(`kubectl logs -n ${ns} --all-containers --tail=200 --selector='' || true`);
    }
    res.note = `Investigate crashing service${svc ? ` '${svc}'` : ''} in namespace '${ns}'`;
    return res;
  }

  res.intent = 'unknown';
  res.note = 'Command not recognized; try one of the supported patterns.';
  return res;
}

function runCommands(cmds, callback) {
  const out = [];
  let idx = 0;

  function next() {
    if (idx >= cmds.length) return callback(null, out.join('\n---\n'));
    const c = cmds[idx++];
    exec(c, { maxBuffer: 10 * 1024 * 1024 }, (err, stdout, stderr) => {
      out.push(`$ ${c}\n${stdout}${stderr}`);
      if (err) {
        return callback(err, out.join('\n---\n'));
      }
      next();
    });
  }
  next();
}

if (require.main === module) {
  const app = express();
  app.use(bodyParser.json());

  app.post('/command', async (req, res) => {
    const { text } = req.body || {};
    if (!text) return res.status(400).json({ error: 'text required' });
    const parsed = parseCommand(text);
    const run = req.query.run === 'true';
    if (run) {
      if (process.env.ALLOW_KUBECTL !== '1') {
        return res.status(403).json({ error: 'Execution disabled. Set ALLOW_KUBECTL=1 to enable.' });
      }
      try {
        runCommands(parsed.kubectl, (err, output) => {
          if (err) return res.status(500).json({ error: err.message, output });
          res.json({ parsed, output });
        });
      } catch (e) {
        res.status(500).json({ error: e.message });
      }
    } else {
      res.json({ parsed });
    }
  });

  const port = process.env.PORT || 3000;
  app.listen(port, () => console.log(`MCP Kubernetes server listening on ${port}`));
}

module.exports = { parseCommand, runCommands };
