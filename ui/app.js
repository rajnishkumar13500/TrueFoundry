document.addEventListener("DOMContentLoaded", () => {
  const btnTrigger = document.getElementById("btn-trigger");
  const btnRetest = document.getElementById("btn-retest");
  const approvalModal = document.getElementById("approval-modal");
  const btnCloseModal = document.getElementById("btn-close-modal");
  const btnAllow = document.getElementById("btn-allow");
  const btnDeny = document.getElementById("btn-deny");
  const checkpointBadge = document.getElementById("checkpoint-badge");
  const timestampEl = document.getElementById("incident-timestamp");

  // Format current UTC time
  const now = new Date();
  if (timestampEl) {
    timestampEl.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  }

  // Open approval modal
  const openApprovalModal = () => {
    approvalModal.style.display = "flex";
  };

  const closeApprovalModal = () => {
    approvalModal.style.display = "none";
  };

  if (btnCloseModal) btnCloseModal.addEventListener("click", closeApprovalModal);

  if (btnAllow) {
    btnAllow.addEventListener("click", () => {
      closeApprovalModal();
      checkpointBadge.textContent = "Authorized & Deployed";
      checkpointBadge.className = "step-status status-success";
      alert("✅ TrueForge Checkpoint: Human authorization recorded. Consequential action executed on controlled production environment.");
    });
  }

  if (btnDeny) {
    btnDeny.addEventListener("click", () => {
      closeApprovalModal();
      checkpointBadge.textContent = "Denied by Operator";
      checkpointBadge.className = "step-status status-danger";
      alert("🛑 Action denied by operator. Agent returned to replanning loop.");
    });
  }

  // Trigger loop animation
  if (btnTrigger) {
    btnTrigger.addEventListener("click", () => {
      btnTrigger.disabled = true;
      btnTrigger.innerHTML = `<span class="btn-icon">⏳</span> Executing Agent Loop...`;

      const steps = [
        "step-remember",
        "step-reason",
        "step-act",
        "step-observe",
        "step-critique",
        "step-human",
        "step-store"
      ];

      // Reset
      steps.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.style.opacity = "0.4";
      });

      let current = 0;
      const interval = setInterval(() => {
        if (current < steps.length) {
          const el = document.getElementById(steps[current]);
          if (el) {
            el.style.opacity = "1";
            el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
          }
          current++;
        } else {
          clearInterval(interval);
          btnTrigger.disabled = false;
          btnTrigger.innerHTML = `<span class="btn-icon">▶</span> Run Investigation Loop`;
          openApprovalModal();
        }
      }, 700);
    });
  }

  // Retest button
  if (btnRetest) {
    btnRetest.addEventListener("click", () => {
      btnRetest.innerHTML = "⏳ Benchmarking...";
      setTimeout(() => {
        btnRetest.innerHTML = `<span class="btn-icon">🔄</span> Re-run Benchmark`;
        alert("Benchmark confirmed: p95 latency = 0.054ms. Zero regressions detected.");
      }, 1200);
    });
  }
});
