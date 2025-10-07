// interactivity for FourTwenty Analytics index page

// interactivity at browser open - Google Tag Manager, etc.

// Google Tag Manager
(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-WVC4SNLB');
// End Google Tag Manager

// Load and render README.md as HTML using marked.js
async function loadReadme() {
  const readmeDiv = document.getElementById('readme-container');
  if (!readmeDiv) return;
  try {
    const response = await fetch('./README.md');
    if (!response.ok) {
      throw new Error('README.md not found');
    }
    const md = await response.text();
    if (typeof marked === 'undefined') {
      // If marked isn't available, render Markdown as preformatted text
      readmeDiv.innerHTML = '<pre>' + escapeHtml(md) + '</pre>';
    } else {
      readmeDiv.innerHTML = marked.parse(md);
    }
  } catch (error) {
    readmeDiv.innerHTML = '<p style="color:#888;"><em>README.md not found.</em></p>';
  }
}

function escapeHtml(unsafe) {
  return unsafe.replace(/[&<"'`=\/]/g, function (s) {
    return ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;',
      '`': '&#96;',
      '=': '&#61;',
      '/': '&#x2F;'
    })[s];
  });
}

// DOMContentLoaded event listener to set up form interactivity
document.addEventListener("DOMContentLoaded", () => {
  // Wire up elements and defer README loading until user requests it
  const form = document.getElementById("broadcastForm");

  const showReadmeBtn = document.getElementById('showReadmeBtn');
  const hideReadmeBtn = document.getElementById('hideReadmeBtn');
  const readmeSection = document.getElementById('readmeSection');

  // Modal controls
  const openBtn = document.getElementById('openBroadcastBtn');
  const closeBtn = document.getElementById('closeBroadcastBtn');
  const modal = document.getElementById('broadcastModal');

  function openModal() {
    if (!modal) return;
    modal.setAttribute('aria-hidden', 'false');
    // focus first input when available
    setTimeout(() => {
      const firstInput = document.querySelector('#broadcastForm input, #broadcastForm textarea, #broadcastForm select');
      if (firstInput) firstInput.focus();
    }, 50);
  }

  function closeModal() {
    if (!modal) return;
    modal.setAttribute('aria-hidden', 'true');
  }

  if (openBtn) openBtn.addEventListener('click', openModal);
  if (closeBtn) closeBtn.addEventListener('click', closeModal);

  // close when clicking outside modal content
  if (modal) {
    modal.addEventListener('click', (e) => {
      if (e.target === modal) closeModal();
    });
    // close on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeModal();
    });
  }

  // Wire workflow modal button and add accessible open/close helpers
  const openWorkflowBtn = document.getElementById('openWorkflowBtn');
  const workflowModal = document.getElementById('workflowModal');
  const closeWorkflowBtn = document.getElementById('closeWorkflowBtn');

  function openWorkflowModal() {
    if (!workflowModal) return;
    workflowModal.setAttribute('aria-hidden', 'false');
    // focus first input in form
    setTimeout(() => {
      const first = workflowModal.querySelector('#workflowForm input, #workflowForm textarea, #workflowForm select');
      if (first) first.focus();
    }, 50);
  }

  function closeWorkflowModal() {
    if (!workflowModal) return;
    workflowModal.setAttribute('aria-hidden', 'true');
  }

  if (openWorkflowBtn) openWorkflowBtn.addEventListener('click', openWorkflowModal);
  if (closeWorkflowBtn) closeWorkflowBtn.addEventListener('click', closeWorkflowModal);

  // close when clicking outside modal content
  if (workflowModal) {
    workflowModal.addEventListener('click', (e) => {
      if (e.target === workflowModal) closeWorkflowModal();
    });
    // close on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeWorkflowModal();
    });
  }

  // README show/hide
  if (showReadmeBtn) {
    showReadmeBtn.addEventListener('click', async () => {
      // load content once, then show
      await loadReadme();
      if (readmeSection) readmeSection.hidden = false;
      // scroll into view
      readmeSection?.scrollIntoView({ behavior: 'smooth' });
    });
  }
  if (hideReadmeBtn) {
    hideReadmeBtn.addEventListener('click', () => {
      if (readmeSection) readmeSection.hidden = true;
    });
  }

  // Modules / Constellation show/hide
  const showModulesBtn = document.getElementById('showModulesBtn');
  const hideModulesBtn = document.getElementById('hideModulesBtn');
  const modulesSection = document.getElementById('modulesSection');
  const modulesContainer = document.getElementById('modules-container');

  async function loadModulesYaml() {
    try {
      const resp = await fetch('./seeds/modules.yml');
      if (!resp.ok) throw new Error('modules.yml not found');
      const text = await resp.text();
      // parse YAML using js-yaml
      const obj = window.jsyaml ? window.jsyaml.load(text) : null;
      return obj;
    } catch (e) {
      console.warn('Failed to load modules.yml', e);
      return null;
    }
  }

  async function renderModules() {
    const data = await loadModulesYaml();
    modulesContainer.innerHTML = '';
    if (!data) {
      modulesContainer.innerHTML = '<p style="color:#888;"><em>modules.yml not available.</em></p>';
      return;
    }
    const list = document.createElement('ul');
    // If YAML parsed to an array (sequence), iterate entries
    if (Array.isArray(data)) {
      data.forEach(entry => {
        const li = document.createElement('li');
        const emoji = document.createElement('span');
        emoji.textContent = entry.emoji ? entry.emoji + ' ' : '';
        const title = document.createElement('strong');
        title.textContent = entry.name || entry.id || 'Unnamed';
        li.appendChild(emoji);
        li.appendChild(title);
        if (entry.orbit) {
          const meta = document.createElement('span');
          meta.style.marginLeft = '8px';
          meta.style.color = '#666';
          meta.textContent = entry.orbit;
          li.appendChild(meta);
        }
        if (entry.pages_url) {
          const a = document.createElement('a');
          a.href = entry.pages_url;
          a.target = '_blank';
          a.rel = 'noopener noreferrer';
          a.style.marginLeft = '10px';
          a.textContent = 'site';
          li.appendChild(a);
        }
        if (entry.description) {
          const desc = document.createElement('div');
          desc.style.fontSize = '0.95rem';
          desc.style.color = '#444';
          desc.textContent = entry.description;
          li.appendChild(desc);
        }
        list.appendChild(li);
      });
    } else if (typeof data === 'object') {
      // mapping: iterate keys
      Object.keys(data).forEach(key => {
        const entry = data[key];
        const li = document.createElement('li');
        li.textContent = (entry.name || entry.title || key) + (entry.description ? ' — ' + entry.description : '');
        list.appendChild(li);
      });
    }
    modulesContainer.appendChild(list);
  }

  if (showModulesBtn) showModulesBtn.addEventListener('click', async () => {
    await renderModules();
    if (modulesSection) modulesSection.hidden = false;
    modulesSection?.scrollIntoView({ behavior: 'smooth' });
  });
  if (hideModulesBtn) hideModulesBtn.addEventListener('click', () => { if (modulesSection) modulesSection.hidden = true; });

  // Signals: archive.latest.json viewer
  const showSignalsBtn = document.getElementById('showSignalsBtn');
  const hideSignalsBtn = document.getElementById('hideSignalsBtn');
  const signalsSection = document.getElementById('signalsSection');
  const signalsContainer = document.getElementById('signals-container');

  async function loadArchiveSignals() {
    try {
      const resp = await fetch('./signals/archive.latest.json');
      if (!resp.ok) throw new Error('signals/archive.latest.json not found');
      const data = await resp.json();
      return data;
    } catch (e) {
      console.warn('Failed to load archive signals', e);
      return null;
    }
  }

  function renderSignalCards(signals) {
    signalsContainer.innerHTML = '';
    if (!signals || !Array.isArray(signals) || signals.length === 0) {
      signalsContainer.innerHTML = '<p style="color:#888;"><em>No signals available.</em></p>';
      return;
    }
    // sort by timestamp-like field if present (attempt multiple common keys)
    signals.sort((a,b) => {
      const tA = new Date(a.ts || a.timestamp || a.date || a.broadcast_ts || 0).getTime();
      const tB = new Date(b.ts || b.timestamp || b.date || b.broadcast_ts || 0).getTime();
      return tB - tA;
    });

    signals.forEach(sig => {
      const card = document.createElement('article');
      card.className = 'signal-card';

      // Date
      const dateLine = document.createElement('div');
      dateLine.className = 'signal-date';
      const dateVal = sig.date || sig.ts || sig.timestamp || sig.broadcast_ts || '';
      dateLine.textContent = dateVal ? new Date(dateVal).toLocaleString() : '';

      // Status icons
      const statusLine = document.createElement('div');
      statusLine.className = 'signal-status';
      if (Array.isArray(sig.status_icons) && sig.status_icons.length) {
        sig.status_icons.forEach(icon => {
          const span = document.createElement('span');
          span.className = 'status-icon';
          span.textContent = icon; // assume emoji or short text
          statusLine.appendChild(span);
        });
      }

      // Broadcast header (rating and name)
      const header = document.createElement('div');
      header.className = 'signal-header';

      const rating = document.createElement('span');
      rating.className = 'signal-rating';
      const bcast = sig.broadcast || sig.broadcast_data || {};
      rating.textContent = (bcast.rating !== undefined && bcast.rating !== null) ? ('★ ' + bcast.rating) : '';

      const name = document.createElement('h3');
      name.className = 'signal-title';
      name.textContent = bcast.name || sig.broadcast_name || sig.title || sig.name || sig.id || 'Signal';

      header.appendChild(rating);
      header.appendChild(name);

      // Summary
      const summary = document.createElement('p');
      summary.className = 'signal-summary';
      summary.textContent = bcast.summary || sig.broadcast_summary || sig.summary || sig.description || '';

      card.appendChild(dateLine);
      card.appendChild(statusLine);
      card.appendChild(header);
      card.appendChild(summary);

      // optional artifact link(s)
      if (sig.artifactGitLink || sig.repo_url || sig.pages_url) {
        const link = document.createElement('a');
        link.href = sig.artifactGitLink || sig.repo_url || sig.pages_url;
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.textContent = 'Open artifact';
        card.appendChild(link);
      }

      signalsContainer.appendChild(card);
    });
  }

  if (showSignalsBtn) showSignalsBtn.addEventListener('click', async () => {
    const data = await loadArchiveSignals();
    // support either an object with items array or an array directly
    const items = Array.isArray(data) ? data : (data && data.items) ? data.items : null;
    renderSignalCards(items);
    if (signalsSection) signalsSection.hidden = false;
    signalsSection?.scrollIntoView({ behavior: 'smooth' });
  });
  if (hideSignalsBtn) hideSignalsBtn.addEventListener('click', () => { if (signalsSection) signalsSection.hidden = true; });

  // Dynamic actions: try to load data/actions.json to create more buttons
  (async function loadDynamicActions() {
    try {
      const resp = await fetch('./data/actions.json');
      if (!resp.ok) return;
      const actions = await resp.json();
      if (!Array.isArray(actions)) return;
      const container = document.getElementById('dynamicActions');
      actions.forEach(act => {
        const btn = document.createElement('button');
        btn.className = 'action-button';
        btn.textContent = act.label || act.name || 'Action';
        btn.addEventListener('click', () => {
          try { window.open(act.url, '_blank'); } catch (e) { console.warn('action failed', e); }
        });
        container.appendChild(btn);
      });
    } catch (e) {
      // quietly ignore missing actions file
    }
  })();

  // Build workflow form inside the workflow modal (acts like the broadcast form)
  try {
    const workflowModalBody = document.querySelector('#workflowModal .modal-body');
    if (workflowModalBody) {
      // create form element
      const wfForm = document.createElement('form');
      wfForm.id = 'workflowForm';

      const wfFields = [
        { label: 'Workflow ID', type: 'text', id: 'workflowId' },
        { label: 'Workflow Name', type: 'text', id: 'workflowName' },
        { label: 'Description', type: 'textarea', id: 'workflowDescription' },
        { label: 'Type', type: 'text', id: 'workflowType' },
        { label: 'Creation Date', type: 'date', id: 'workflowCreationDate' },
        { label: 'Status', type: 'text', id: 'workflowStatus' },
        { label: 'Owner', type: 'text', id: 'workflowOwner' },
        { label: 'Last Updated', type: 'date', id: 'workflowLastUpdated' },
        { label: 'Steps (integer)', type: 'number', id: 'workflowStepsInteger' },
        { label: 'Steps (array, comma-separated)', type: 'textarea', id: 'workflowStepsArray' },
        { label: 'Artifacts (array, comma-separated)', type: 'textarea', id: 'workflowArtifactsArray' }
      ];

      wfFields.forEach(field => {
        const label = document.createElement('label');
        label.htmlFor = field.id;
        label.textContent = field.label;

        let input;
        if (field.type === 'textarea') {
          input = document.createElement('textarea');
        } else {
          input = document.createElement('input');
          input.type = field.type;
        }
        input.id = field.id;
        input.name = field.id;

        wfForm.appendChild(label);
        wfForm.appendChild(input);
      });

      const submitButton = document.createElement('button');
      submitButton.type = 'submit';
      submitButton.textContent = 'Submit Workflow';
      wfForm.appendChild(submitButton);

      // insert the form at the top of modal body, keep the existing workflow image below
      workflowModalBody.insertBefore(wfForm, workflowModalBody.firstChild);

      // handle submit
      wfForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
          workflow_id: document.getElementById('workflowId')?.value || '',
          workflow_name: document.getElementById('workflowName')?.value || '',
          workflow_description: document.getElementById('workflowDescription')?.value || '',
          workflow_type: document.getElementById('workflowType')?.value || '',
          workflow_creation_date: document.getElementById('workflowCreationDate')?.value || '',
          workflow_status: document.getElementById('workflowStatus')?.value || '',
          workflow_owner: document.getElementById('workflowOwner')?.value || '',
          workflow_last_updated: document.getElementById('workflowLastUpdated')?.value || '',
          workflow_steps_integer: parseInt(document.getElementById('workflowStepsInteger')?.value || '0', 10) || 0,
          workflow_steps_array: (document.getElementById('workflowStepsArray')?.value || '').split(',').map(s=>s.trim()).filter(Boolean),
          workflow_artifacts_array: (document.getElementById('workflowArtifactsArray')?.value || '').split(',').map(s=>s.trim()).filter(Boolean)
        };

        // dataLayer for GTM
        try {
          window.dataLayer = window.dataLayer || [];
          const evt = Object.assign({ event: 'workflow_submit', timestamp: new Date().toISOString() }, payload);
          window.dataLayer.push(evt);
          console.log('Pushed workflow to dataLayer:', evt);
        } catch (err) {
          console.warn('Failed to push workflow to dataLayer', err);
        }

        // POST to local workflow endpoint (mirrors broadcast API)
        try {
          const resp = await fetch('http://127.0.0.1:5002/api/workflow', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });
          const result = await resp.json().catch(()=>({}));
          if (resp.ok) {
            const successDiv = document.createElement('div');
            successDiv.style.color = 'green';
            successDiv.textContent = `Workflow created: ${result.workflow_id || payload.workflow_id || 'ok'}`;
            wfForm.prepend(successDiv);
          } else {
            const errDiv = document.createElement('div');
            errDiv.style.color = 'red';
            errDiv.textContent = `Failed: ${result.error || resp.statusText || 'unknown'}`;
            wfForm.prepend(errDiv);
          }
        } catch (err) {
          const errDiv = document.createElement('div');
          errDiv.style.color = 'red';
          errDiv.textContent = `Failed to reach workflow server: ${err.message}`;
          wfForm.prepend(errDiv);
        }
      });
    }
  } catch (e) {
    // ignore any UI build errors
    console.warn('Could not build workflow form', e);
  }

  const fields = [
    { label: "Date", type: "date", id: "date" },
        { label: "Module ID", type: "text", id: "moduleId" },
        { label: "Broadcast Rating", type: "text", id: "broadcastRating" },
        { label: "Broadcast Name", type: "text", id: "broadcastName" },
        { label: "Broadcast Summary", type: "textarea", id: "broadcastSummary" },
        { label: "Status ID", type: "text", id: "statusId" },
        { label: "Artifact Git Link", type: "url", id: "artifactGitLink" },
        { label: "Tags Keys", type: "text", id: "tagsKeys" }
    ];

    fields.forEach(field => {
        const label = document.createElement("label");
        label.htmlFor = field.id;
        label.textContent = field.label;

        let input;
        if (field.type === "textarea") {
            input = document.createElement("textarea");
        } else {
            input = document.createElement("input");
            input.type = field.type;
        }
        input.id = field.id;
        input.name = field.id;

        form.appendChild(label);
        form.appendChild(input);
    });

    const submitButton = document.createElement("button");
    submitButton.type = "submit";
    submitButton.textContent = "Submit";
    form.appendChild(submitButton);

    form.addEventListener("submit", async (event) => {
    event.preventDefault();

    // collect form data
    const formData = {
  // broadcastId and timestamp are intentionally omitted: server will generate them
      date: document.getElementById('date')?.value || '',
      moduleId: document.getElementById('moduleId')?.value || '',
      broadcastRating: document.getElementById('broadcastRating')?.value || '',
      broadcastName: document.getElementById('broadcastName')?.value || '',
      broadcastSummary: document.getElementById('broadcastSummary')?.value || '',
      statusId: document.getElementById('statusId')?.value || '',
      artifactGitLink: document.getElementById('artifactGitLink')?.value || '',
      tagsKeys: (document.getElementById('tagsKeys')?.value || '').split(',').map(s => s.trim()).filter(Boolean)
    };

    // Prepare payload for GTM / dataLayer so tags can react to this interaction
    try {
      window.dataLayer = window.dataLayer || [];
      const payload = Object.assign({ event: 'broadcast_submit', timestamp: new Date().toISOString() }, formData);
      window.dataLayer.push(payload);
      console.log('Pushed to dataLayer:', payload);
    } catch (e) {
      console.warn('Failed to push to dataLayer', e);
    }

    // Post to local broadcast server
    try {
      const resp = await fetch('http://127.0.0.1:5002/api/broadcast', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const result = await resp.json();
      if (resp.ok) {
        // replace alert with inline success message inside modal
        const successDiv = document.createElement('div');
        successDiv.style.color = 'green';
        successDiv.textContent = `Broadcast created: ${result.broadcast_id}`;
        document.querySelector('#broadcastForm').prepend(successDiv);
      } else {
        const errDiv = document.createElement('div');
        errDiv.style.color = 'red';
        errDiv.textContent = `Failed: ${result.error || 'unknown'}`;
        document.querySelector('#broadcastForm').prepend(errDiv);
      }
    } catch (e) {
      const errDiv = document.createElement('div');
      errDiv.style.color = 'red';
      errDiv.textContent = `Failed to reach broadcast server: ${e.message}`;
      document.querySelector('#broadcastForm').prepend(errDiv);
    }
  });
});