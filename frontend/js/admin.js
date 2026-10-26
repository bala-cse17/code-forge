/**
 * CODE COMBAT Pro - Admin Operations & Authentication Module
 */

const Admin = {
  token: '',
  adminId: 'admincse',
  tierLocks: { easy: false, medium: false, hard: false },

  getToken() {
    return this.token || '';
  },

  getAdminId() {
    return this.adminId || 'admincse';
  },

  isAuthenticated() {
    return Boolean(this.token);
  },

  lock() {
    this.token = '';
    this.adminId = 'admincse';
    sessionStorage.removeItem('cc_admin_token');
    sessionStorage.removeItem('cc_admin_id');
    localStorage.removeItem('cc_admin_token');
    localStorage.removeItem('cc_admin_id');

    const idInput = document.getElementById('admin-login-id');
    const passInput = document.getElementById('admin-login-pass');
    const authErrorEl = document.getElementById('admin-auth-error');
    if (idInput) idInput.value = '';
    if (passInput) passInput.value = '';
    if (authErrorEl) {
      authErrorEl.textContent = '';
      authErrorEl.style.display = 'none';
    }

    const gateEl = document.getElementById('admin-auth-gate');
    const portalEl = document.getElementById('admin-portal-content');
    if (gateEl) gateEl.style.display = 'block';
    if (portalEl) portalEl.style.display = 'none';
  },

  getAuthHeaders() {
    const token = this.getToken();
    const headers = { 'Content-Type': 'application/json' };
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  },

  checkAuthUI() {
    const gateEl = document.getElementById('admin-auth-gate');
    const portalEl = document.getElementById('admin-portal-content');
    const displayIdEl = document.getElementById('admin-display-id');
    const authErrorEl = document.getElementById('admin-auth-error');

    if (authErrorEl) authErrorEl.style.display = 'none';

    if (this.isAuthenticated()) {
      if (gateEl) gateEl.style.display = 'none';
      if (portalEl) portalEl.style.display = 'flex';
      if (displayIdEl) displayIdEl.textContent = this.getAdminId();
      this.loadSets();
      this.loadTierLocks();
      this.loadProctorLogs();
      this.loadAnalytics();
      this.loadParticipants();
      this.loadAuditLogs();
      this.checkHealth();
    } else {
      if (gateEl) gateEl.style.display = 'block';
      if (portalEl) portalEl.style.display = 'none';
      const idInput = document.getElementById('admin-login-id');
      if (idInput && App.currentView === 'admin') {
        setTimeout(() => idInput.focus(), 50);
      }
    }
  },

  async handleLogin(e) {
    if (e) e.preventDefault();
    const idInput = document.getElementById('admin-login-id');
    const passInput = document.getElementById('admin-login-pass');
    const errorEl = document.getElementById('admin-auth-error');

    const adminId = idInput ? idInput.value.trim() : '';
    const password = passInput ? passInput.value.trim() : '';

    if (!adminId || !password) {
      if (errorEl) {
        errorEl.textContent = 'Please enter both Administrator ID and Password.';
        errorEl.style.display = 'block';
      }
      return;
    }

    try {
      const res = await fetch('/api/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          admin_id: adminId,
          password: password
        })
      });

      const data = await res.json();
      if (data.authenticated && data.token) {
        this.token = data.token;
        this.adminId = data.admin_id || adminId;

        if (idInput) idInput.value = '';
        if (passInput) passInput.value = '';
        if (errorEl) errorEl.style.display = 'none';

        this.checkAuthUI();
        App.showToast(`Admin Portal Unlocked. Welcome, ${data.admin_id || adminId}!`, 'success');
      } else {
        const errMsg = data.error || 'Invalid Administrator ID or Password.';
        if (errorEl) {
          errorEl.textContent = errMsg;
          errorEl.style.display = 'block';
        }
        App.showToast(errMsg, 'error');
      }
    } catch (err) {
      const msg = 'Login request failed: ' + err.message;
      if (errorEl) {
        errorEl.textContent = msg;
        errorEl.style.display = 'block';
      }
      App.showToast(msg, 'error');
    }
  },

  logout() {
    this.lock();
    this.checkAuthUI();
    App.showToast('Admin Portal locked successfully.', 'info');
  },

  async exportAllJSON() {
    try {
      const res = await fetch('/api/admin/export', {
        headers: this.getAuthHeaders()
      });
      const data = await res.json();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `code_combat_backup_${new Date().toISOString().slice(0,10)}.json`;
      a.click();
      URL.revokeObjectURL(url);
      App.showToast('JSON database export downloaded.', 'success');
    } catch (e) {
      App.showToast('Export failed: ' + e.message, 'error');
    }
  },

  async loadSets() {
    try {
      const res = await fetch('/api/admin/sets', {
        headers: this.getAuthHeaders()
      });
      if (!res.ok) return;
      const data = await res.json();
      const sel = document.getElementById('admin-set-select');
      if (sel && data.sets) {
        sel.innerHTML = data.sets.map(s => `
          <option value="${s.id}" ${s.id === data.active_set ? 'selected' : ''}>${s.name}</option>
        `).join('');
      }
    } catch (e) {
      console.warn('Error loading problem sets:', e);
    }
  },

  async switchProblemSet() {
    const sel = document.getElementById('admin-set-select');
    const resetCheck = document.getElementById('admin-set-reset-check');
    if (!sel) return;

    const setId = sel.value;
    const resetData = resetCheck ? resetCheck.checked : true;

    try {
      const res = await fetch('/api/admin/switch-set', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          token: this.getToken(),
          set_id: setId,
          reset_data: resetData
        })
      });

      const data = await res.json();
      if (data.success) {
        App.showToast(data.message || `Switched to ${setId.toUpperCase()}!`, 'success');

        if (resetData) {
          App.participant = null;
          localStorage.removeItem('cc_participant');
          const badge = document.getElementById('user-badge');
          if (badge) badge.style.display = 'none';
        }

        App.loadProblems();
        App.loadLeaderboard();
        this.checkHealth();
      } else {
        if (res.status === 401) {
          this.logout();
          App.showToast('Admin session expired. Please log in again.', 'warning');
        } else {
          App.showToast('Switch set failed: ' + (data.error || 'Unknown error'), 'error');
        }
      }
    } catch (e) {
      App.showToast('Network error switching set: ' + e.message, 'error');
    }
  },

  async loadTierLocks() {
    try {
      const res = await fetch('/api/admin/tier-locks', {
        headers: this.getAuthHeaders()
      });
      if (!res.ok) return;
      const data = await res.json();
      if (data.tier_locks) {
        this.tierLocks = data.tier_locks;
        this.renderTierLocksUI();
      }
    } catch (e) {
      console.warn('Error loading tier locks:', e);
    }
  },

  renderTierLocksUI() {
    const tiers = [
      { id: 'easy', num: 1, name: 'Easy', color: 'var(--accent-green)', badgeBg: 'rgba(16,185,129,0.15)', badgeBorder: 'var(--accent-green)', badgeColor: 'var(--accent-green)' },
      { id: 'medium', num: 2, name: 'Medium', color: 'var(--accent-amber)', badgeBg: 'rgba(245,158,11,0.15)', badgeBorder: 'var(--accent-amber)', badgeColor: 'var(--accent-amber)' },
      { id: 'hard', num: 3, name: 'Hard', color: 'var(--accent-red)', badgeBg: 'rgba(239,68,68,0.15)', badgeBorder: 'var(--accent-red)', badgeColor: 'var(--accent-red)' }
    ];

    tiers.forEach(t => {
      const isLocked = Boolean(this.tierLocks[t.id]);
      const badge = document.getElementById(`badge-lock-${t.id}`);
      const btn = document.getElementById(`btn-toggle-${t.id}`);
      const card = document.getElementById(`admin-tier-card-${t.id}`);

      if (badge) {
        if (isLocked) {
          badge.textContent = '🔒 LOCKED';
          badge.style.background = 'rgba(239,68,68,0.15)';
          badge.style.borderColor = 'var(--accent-red)';
          badge.style.color = 'var(--accent-red)';
        } else {
          badge.textContent = '🔓 ACTIVE';
          badge.style.background = t.badgeBg;
          badge.style.borderColor = t.badgeBorder;
          badge.style.color = t.badgeColor;
        }
      }

      if (btn) {
        if (isLocked) {
          btn.innerHTML = `🔓 Unlock Round ${t.num} (${t.name})`;
          btn.className = 'btn btn-primary';
          btn.style.background = 'linear-gradient(135deg, var(--accent-cyan), #0070f3)';
          btn.style.color = '#fff';
        } else {
          btn.innerHTML = `🔒 Lock Round ${t.num} (${t.name})`;
          btn.className = 'btn btn-secondary';
          btn.style.background = 'transparent';
          btn.style.color = 'var(--accent-red)';
          btn.style.borderColor = 'rgba(239,68,68,0.4)';
        }
      }

      if (card) {
        if (isLocked) {
          card.style.borderColor = 'rgba(239,68,68,0.4)';
          card.style.background = 'rgba(239,68,68,0.03)';
        } else {
          card.style.borderColor = `rgba(0, 242, 254, 0.25)`;
          card.style.background = 'var(--bg-primary)';
        }
      }
    });
  },

  async toggleTierLock(tier) {
    const currentLocked = Boolean(this.tierLocks[tier]);
    const nextLocked = !currentLocked;

    try {
      const res = await fetch('/api/admin/toggle-tier-lock', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          token: this.getToken(),
          tier: tier,
          locked: nextLocked
        })
      });

      const data = await res.json();
      if (data.success && data.tier_locks) {
        this.tierLocks = data.tier_locks;
        this.renderTierLocksUI();
        App.loadProblems();
        App.showToast(data.message || `Round (${tier.toUpperCase()}) updated!`, 'success');
      } else {
        App.showToast(data.error || 'Failed to update round lock status.', 'error');
      }
    } catch (e) {
      App.showToast('Network error updating round lock: ' + e.message, 'error');
    }
  },

  async applyTierPreset(preset) {
    try {
      const res = await fetch('/api/admin/toggle-tier-lock', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          token: this.getToken(),
          preset: preset
        })
      });

      const data = await res.json();
      if (data.success && data.tier_locks) {
        this.tierLocks = data.tier_locks;
        this.renderTierLocksUI();
        App.loadProblems();
        App.showToast(data.message || 'Preset applied successfully!', 'success');
      } else {
        App.showToast(data.error || 'Failed to apply preset.', 'error');
      }
    } catch (e) {
      App.showToast('Network error applying preset: ' + e.message, 'error');
    }
  },

  async handleChangeCredentials(e) {
    if (e) e.preventDefault();
    const currPass = document.getElementById('admin-curr-pass')?.value || '';
    const newId = document.getElementById('admin-new-id')?.value.trim() || '';
    const newPass = document.getElementById('admin-new-pass')?.value || '';
    const confirmPass = document.getElementById('admin-confirm-pass')?.value || '';

    if (!currPass) {
      App.showToast('Please enter your current admin password.', 'warning');
      return;
    }
    if (newPass && newPass.length < 4) {
      App.showToast('New password must be at least 4 characters long.', 'warning');
      return;
    }
    if (newPass && newPass !== confirmPass) {
      App.showToast('New passwords do not match. Please re-enter.', 'error');
      return;
    }

    try {
      const res = await fetch('/api/admin/change-password', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          token: this.getToken(),
          old_password: currPass,
          new_admin_id: newId || undefined,
          new_password: newPass || undefined
        })
      });

      const data = await res.json();
      if (data.success) {
        if (newId) {
          this.adminId = newId;
          const displayIdEl = document.getElementById('admin-display-id');
          if (displayIdEl) displayIdEl.textContent = newId;
        }
        App.showToast('Admin credentials updated successfully!', 'success');
        if (document.getElementById('admin-curr-pass')) document.getElementById('admin-curr-pass').value = '';
        if (document.getElementById('admin-new-id')) document.getElementById('admin-new-id').value = '';
        if (document.getElementById('admin-new-pass')) document.getElementById('admin-new-pass').value = '';
        if (document.getElementById('admin-confirm-pass')) document.getElementById('admin-confirm-pass').value = '';
      } else {
        App.showToast('Update failed: ' + (data.error || 'Incorrect current credentials'), 'error');
      }
    } catch (err) {
      App.showToast('Network error: ' + err.message, 'error');
    }
  },

  async resetCompetition() {
    if (!confirm('⚠️ WARNING: This will permanently wipe ALL participants, scores, submissions, and leaderboard rankings across the competition!\n\nAre you sure you want to proceed?')) {
      return;
    }

    try {
      const res = await fetch('/api/admin/reset', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ token: this.getToken() })
      });
      const data = await res.json();
      if (data.success) {
        App.showToast('Competition completely reset. All points & submissions wiped to 0.', 'success');
        
        // Clear client participant session and scores
        App.participant = null;
        localStorage.removeItem('cc_participant');
        const badge = document.getElementById('user-badge');
        if (badge) badge.style.display = 'none';

        // Refresh views
        App.loadLeaderboard();
        App.loadProblems();
        this.checkHealth();
      } else {
        if (res.status === 401) {
          this.logout();
          App.showToast('Admin session expired. Please log in again.', 'warning');
        } else {
          App.showToast('Reset failed: ' + (data.error || 'Unauthorized'), 'error');
        }
      }
    } catch (e) {
      App.showToast('Reset request error: ' + e.message, 'error');
    }
  },

  async checkHealth() {
    const el = document.getElementById('admin-health-status');
    if (!el) return;
    try {
      const res = await fetch('/api/health');
      const health = await res.json();
      el.innerHTML = `
        <div>Status: <strong>${health.status.toUpperCase()}</strong></div>
        <div>Uptime: ${health.uptime_seconds}s</div>
        <div>Active Problem Set: <strong>${health.active_problem_set ? health.active_problem_set.toUpperCase() : 'SET 1'}</strong></div>
        <div>Python: OK | C: ${health.compilers.c ? health.compilers.c_compiler : 'Not Found'} | Java: ${health.compilers.java ? health.compilers.java_compiler : 'Not Found'}</div>
        <div>Loaded Problems in Active Set: <strong>${health.total_problems}</strong></div>
      `;
    } catch (e) {
      el.innerHTML = `<span style="color:var(--accent-red)">Health check failed: ${e.message}</span>`;
    }
  },

  // ---------------- Real-Time Broadcast & Freeze Controls ----------------

  async sendBroadcast() {
    const textInput = document.getElementById('admin-broadcast-text');
    const severityInput = document.getElementById('admin-broadcast-severity');
    const text = textInput ? textInput.value.trim() : '';
    const severity = severityInput ? severityInput.value : 'info';

    if (!text) {
      App.showToast('Please enter an announcement message.', 'warning');
      return;
    }

    try {
      const res = await fetch('/api/admin/broadcast', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          token: this.getToken(),
          message: text,
          severity: severity
        })
      });

      const data = await res.json();
      if (data.success) {
        App.showToast('Broadcast announcement dispatched to all screens!', 'success');
        if (textInput) textInput.value = '';
      } else {
        App.showToast(data.error || 'Failed to dispatch broadcast.', 'error');
      }
    } catch (e) {
      App.showToast('Network error dispatching broadcast: ' + e.message, 'error');
    }
  },

  async clearBroadcast() {
    try {
      const res = await fetch('/api/admin/broadcast', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          token: this.getToken(),
          clear: true
        })
      });

      const data = await res.json();
      if (data.success) {
        App.showToast('Active broadcast cleared.', 'info');
      }
    } catch (e) {
      App.showToast('Error clearing broadcast: ' + e.message, 'error');
    }
  },

  async toggleFreezeLeaderboard() {
    try {
      const res = await fetch('/api/admin/freeze-leaderboard', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          token: this.getToken()
        })
      });

      const data = await res.json();
      if (data.success) {
        const isFrozen = Boolean(data.is_frozen);
        const badge = document.getElementById('admin-freeze-status-badge');
        const btn = document.getElementById('btn-toggle-freeze');
        if (badge) {
          badge.textContent = isFrozen ? '❄️ FROZEN' : '🟢 LIVE';
          badge.style.background = isFrozen ? 'rgba(0, 242, 254, 0.15)' : 'rgba(16, 185, 129, 0.15)';
          badge.style.borderColor = isFrozen ? 'var(--accent-cyan)' : 'var(--accent-green)';
          badge.style.color = isFrozen ? 'var(--accent-cyan)' : 'var(--accent-green)';
        }
        if (btn) {
          btn.textContent = isFrozen ? '🟢 Unfreeze Leaderboard' : '❄️ Freeze Leaderboard';
          btn.className = isFrozen ? 'btn btn-primary' : 'btn btn-secondary';
        }
        App.showToast(data.message || `Leaderboard ${isFrozen ? 'Frozen' : 'Live'}!`, 'info');
      }
    } catch (e) {
      App.showToast('Error toggling freeze: ' + e.message, 'error');
    }
  },

  async loadProctorLogs() {
    try {
      const res = await fetch('/api/admin/proctor-logs', {
        headers: this.getAuthHeaders()
      });
      if (!res.ok) return;
      const data = await res.json();

      const countsEl = document.getElementById('admin-proctor-counts-list');
      const eventsEl = document.getElementById('admin-proctor-events-list');

      if (countsEl) {
        const counts = data.tab_counts || [];
        if (counts.length === 0) {
          countsEl.innerHTML = '<span style="color:var(--text-muted);">No tab switch infractions recorded.</span>';
        } else {
          countsEl.innerHTML = counts.map(c => `
            <div style="display:flex; justify-content:space-between; padding:0.35rem 0; border-bottom:1px solid rgba(255,255,255,0.05);">
              <span style="font-weight:700; color:#fff;">${c.participant_name}</span>
              <span class="badge" style="background:rgba(239,68,68,0.2); color:#fca5a5; border:1px solid var(--accent-red); font-size:0.75rem;">
                ${c.switch_count} switches
              </span>
            </div>
          `).join('');
        }
      }

      if (eventsEl) {
        const events = (data.tab_switches || []).slice(0, 20);
        if (events.length === 0) {
          eventsEl.innerHTML = '<span style="color:var(--text-muted);">No tab blur events logged yet.</span>';
        } else {
          eventsEl.innerHTML = events.map(e => `
            <div style="padding:0.25rem 0; border-bottom:1px solid rgba(255,255,255,0.03);">
              <span style="color:#ef4444;">[${e.timestamp ? e.timestamp.slice(11,19) : '--:--'}]</span>
              <strong style="color:#fff;">${e.participant_name}</strong> switched tab
            </div>
          `).join('');
        }
      }
    } catch (e) {
      console.warn('Error loading proctor logs:', e);
    }
  },

  async loadAnalytics() {
    try {
      const res = await fetch('/api/admin/analytics', { headers: this.getAuthHeaders() });
      if (!res.ok) return;
      const data = await res.json();
      if (!data.analytics) return;
      const an = data.analytics;

      const pEl = document.getElementById('admin-stat-participants');
      const sEl = document.getElementById('admin-stat-submissions');
      const aEl = document.getElementById('admin-stat-accepted');
      const rEl = document.getElementById('admin-stat-rate');
      const langEl = document.getElementById('admin-lang-breakdown');
      const diffEl = document.getElementById('admin-diff-breakdown');

      if (pEl) pEl.textContent = an.total_participants ?? 0;
      if (sEl) sEl.textContent = an.total_submissions ?? 0;
      if (aEl) aEl.textContent = an.accepted_submissions ?? 0;
      if (rEl) rEl.textContent = `${an.acceptance_rate ?? 0}%`;

      if (langEl) {
        const langs = Object.entries(an.languages || {});
        if (langs.length === 0) {
          langEl.innerHTML = '<span style="color:var(--text-muted);">No submissions recorded yet.</span>';
        } else {
          langEl.innerHTML = langs.map(([l, c]) => `
            <div style="display:flex; justify-content:space-between; margin-bottom:0.35rem;">
              <span style="text-transform:capitalize; color:#fff;">${l}</span>
              <strong style="color:var(--accent-cyan);">${c}</strong>
            </div>
          `).join('');
        }
      }

      if (diffEl) {
        const diffs = Object.entries(an.difficulty_solves || {});
        if (diffs.length === 0) {
          diffEl.innerHTML = '<span style="color:var(--text-muted);">No accepted solves yet.</span>';
        } else {
          diffEl.innerHTML = diffs.map(([d, c]) => `
            <div style="display:flex; justify-content:space-between; margin-bottom:0.35rem;">
              <span style="text-transform:capitalize; color:#fff;">${d}</span>
              <strong style="color:var(--accent-green);">${c}</strong>
            </div>
          `).join('');
        }
      }
    } catch (e) {
      console.warn('Error loading analytics:', e);
    }
  },

  async loadParticipants() {
    try {
      const res = await fetch('/api/participants', { headers: this.getAuthHeaders() });
      if (!res.ok) return;
      const data = await res.json();
      const parts = data.participants || [];
      const tbody = document.getElementById('admin-participants-table-body');
      if (!tbody) return;

      if (parts.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center; color:var(--text-muted); padding:1.5rem;">No participants registered yet.</td></tr>';
        return;
      }

      tbody.innerHTML = parts.map(p => `
        <tr>
          <td><strong style="color:#fff;">${p.name}</strong></td>
          <td><code style="font-family:var(--font-mono); color:var(--accent-cyan); font-size:0.8rem;">${p.reg_no}</code></td>
          <td style="color:var(--text-secondary);">${p.college || '-'}</td>
          <td><span style="font-weight:700; color:var(--accent-cyan);">${p.score || 0} pts</span></td>
          <td>
            <div style="display:flex; gap:0.4rem;">
              <button class="btn btn-secondary" style="font-size:0.75rem; padding:0.2rem 0.5rem;" onclick="Admin.resetParticipantScore('${p.id}')" title="Reset score to 0">🔄 Reset</button>
              <button class="btn btn-danger" style="font-size:0.75rem; padding:0.2rem 0.5rem; color:var(--accent-red); border-color:var(--accent-red); background:transparent;" onclick="Admin.deleteParticipant('${p.id}')" title="Delete participant">🗑️</button>
            </div>
          </td>
        </tr>
      `).join('');
    } catch (e) {
      console.warn('Error loading participants:', e);
    }
  },

  async resetParticipantScore(pid) {
    if (!confirm('Are you sure you want to reset this participant’s score and solved problems to 0?')) return;
    try {
      const res = await fetch('/api/admin/participant/reset-score', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ token: this.getToken(), participant_id: pid })
      });
      const data = await res.json();
      if (data.success) {
        App.showToast('Participant score reset to 0.', 'success');
        this.loadParticipants();
        App.loadLeaderboard();
      } else {
        App.showToast(data.error || 'Failed to reset score', 'error');
      }
    } catch (e) {
      App.showToast('Network error: ' + e.message, 'error');
    }
  },

  async deleteParticipant(pid) {
    if (!confirm('Permanently delete this participant and all associated submissions?')) return;
    try {
      const res = await fetch('/api/admin/participant/delete', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({ token: this.getToken(), participant_id: pid })
      });
      const data = await res.json();
      if (data.success) {
        App.showToast('Participant removed successfully.', 'success');
        this.loadParticipants();
        App.loadLeaderboard();
      } else {
        App.showToast(data.error || 'Failed to delete participant', 'error');
      }
    } catch (e) {
      App.showToast('Network error: ' + e.message, 'error');
    }
  },

  async loadAuditLogs() {
    try {
      const res = await fetch('/api/admin/audit-logs', { headers: this.getAuthHeaders() });
      if (!res.ok) return;
      const data = await res.json();
      const logs = data.logs || [];
      const tbody = document.getElementById('admin-audit-table-body');
      if (!tbody) return;

      if (logs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" style="text-align:center; color:var(--text-muted); padding:1rem;">No audit logs recorded yet.</td></tr>';
        return;
      }

      tbody.innerHTML = logs.map(l => `
        <tr>
          <td style="font-family:var(--font-mono); font-size:0.75rem; color:var(--text-muted);">${(l.timestamp || '').replace('T', ' ').slice(0, 19)}</td>
          <td><span class="badge badge-easy" style="font-size:0.7rem;">${l.action}</span></td>
          <td style="color:var(--text-secondary); font-size:0.8rem;">${l.details}</td>
        </tr>
      `).join('');
    } catch (e) {
      console.warn('Error loading audit logs:', e);
    }
  },

  async createContest(e) {
    if (e) e.preventDefault();
    const title = document.getElementById('admin-contest-title')?.value.trim();
    const desc = document.getElementById('admin-contest-desc')?.value.trim();
    const status = document.getElementById('admin-contest-status')?.value || 'upcoming';

    if (!title) {
      App.showToast('Contest title is required.', 'warning');
      return;
    }

    const cid = 'contest_' + Date.now().toString(36);
    try {
      const res = await fetch('/api/admin/contest/create', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          token: this.getToken(),
          id: cid,
          title: title,
          description: desc,
          status: status
        })
      });
      const data = await res.json();
      if (data.success) {
        App.showToast(`Contest "${title}" created successfully!`, 'success');
        document.getElementById('admin-contest-title').value = '';
        document.getElementById('admin-contest-desc').value = '';
        this.loadAuditLogs();
      } else {
        App.showToast(data.error || 'Failed to create contest', 'error');
      }
    } catch (err) {
      App.showToast('Network error: ' + err.message, 'error');
    }
  },

  async saveProblem(e) {
    if (e) e.preventDefault();
    const pid = document.getElementById('admin-prob-id')?.value.trim();
    const title = document.getElementById('admin-prob-title')?.value.trim();
    const diff = document.getElementById('admin-prob-diff')?.value || 'Easy';
    const pts = parseInt(document.getElementById('admin-prob-pts')?.value || '100', 10);
    const desc = document.getElementById('admin-prob-desc')?.value.trim();
    const constraints = document.getElementById('admin-prob-constraints')?.value.trim();

    if (!pid || !title || !desc) {
      App.showToast('Problem ID, Title, and Description are required.', 'warning');
      return;
    }

    try {
      const res = await fetch('/api/admin/problem/save', {
        method: 'POST',
        headers: this.getAuthHeaders(),
        body: JSON.stringify({
          token: this.getToken(),
          id: pid,
          title: title,
          difficulty: diff,
          points: pts,
          description: desc,
          constraints: constraints
        })
      });
      const data = await res.json();
      if (data.success) {
        App.showToast(`Problem "${title}" saved successfully!`, 'success');
        this.loadAuditLogs();
        App.loadProblems();
      } else {
        App.showToast(data.error || 'Failed to save problem', 'error');
      }
    } catch (err) {
      App.showToast('Network error: ' + err.message, 'error');
    }
  }
};

window.Admin = Admin;



