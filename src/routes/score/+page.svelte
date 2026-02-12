<script>
  const COLORS = {
    acceptedOnTimeBg: "#2ecc71", // green
    submittedBg: "#e74c3c", // red
    acceptedLateBg: "#3498db", // blue
  };

  const API = {
    baseUrl: "https://codeforces.com/api",
    from: 1,
    count: 10000,
  };

  const PARTICIPANTS = [
    { name: "Nemkin Viktória", handle: "nemkin" },
    { name: "Klevis Imeri", handle: "klevis.cpp" },
  ];

  const PROBLEMS = [
    {
      label: "1A",
      contestId: 118,
      index: "B",
      problemUrl: "https://codeforces.com/contest/118/problem/B",
      solutionUrl: "https://codeforces.com/contest/118/submission/362637816",
      deadline: new Date("2026-02-20T23:59:59+01:00"),
    },
    {
      label: "1B",
      contestId: 1374,
      index: "C",
      problemUrl: "https://codeforces.com/contest/1374/problem/C",
      solutionUrl: "https://codeforces.com/contest/1374/submission/362649274",
      deadline: new Date("2026-02-20T23:59:59+01:00"),
    },
    {
      label: "1C",
      contestId: 1916,
      index: "B",
      problemUrl: "https://codeforces.com/contest/1916/problem/B",
      solutionUrl: "https://codeforces.com/contest/1916/submission/362647570",
      deadline: new Date("2026-02-20T23:59:59+01:00"),
    },
  ];

  let loading = $state(true);
  let errorMsg = $state("");
  let rawByHandle = $state(new Map()); // handle -> submissions array (result from API)
  let fetchedOnce = $state(false);

  function problemKey(contestId, index) {
    return `${contestId}#${index}`;
  }

  function formatDateTime(dateOrMs) {
    const date = typeof dateOrMs === "number" ? new Date(dateOrMs) : dateOrMs;
    return date
      .toLocaleString("sv-SE", {
        timeZone: "Europe/Budapest",
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
      })
      .replace(",", "");
  }

  let problemsWithDeadlines = $derived(
    PROBLEMS.map((p) => ({
      ...p,
      key: problemKey(p.contestId, p.index),
      deadlineMs: p.deadline.getTime(),
      formattedDeadline: formatDateTime(p.deadline),
    })),
  );

  async function fetchUserStatus(handle) {
    const url =
      `${API.baseUrl}/user.status?handle=${encodeURIComponent(handle)}` +
      `&from=${encodeURIComponent(String(API.from))}` +
      `&count=${encodeURIComponent(String(API.count))}`;
    const res = await fetch(url, { method: "GET" });
    if (!res.ok) throw new Error(`HTTP ${res.status} for handle ${handle}`);
    const json = await res.json();
    if (!json || json.status !== "OK" || !Array.isArray(json.result)) {
      throw new Error(`API error for handle ${handle}`);
    }
    return json.result;
  }

  function computeCell(submissions, deadlineMs, contestId) {
    // submissions: array filtered to this (user, problem)
    if (submissions.length === 0) {
      return {
        kind: "empty",
        bg: "",
        lines: [],
        submissionId: null,
      };
    }

    const okSubs = submissions.filter((s) => s?.verdict === "OK");
    const hasOk = okSubs.length > 0;

    // Oldest OK by creationTimeSeconds (if any)
    let oldestOkSec = Infinity;
    let oldestOkSubmission = null;
    for (const s of okSubs) {
      const t = s?.creationTimeSeconds;
      if (typeof t === "number" && t < oldestOkSec) {
        oldestOkSec = t;
        oldestOkSubmission = s;
      }
    }

    // Latest submission by creationTimeSeconds
    let latest = null;
    let latestSec = -Infinity;
    for (const s of submissions) {
      const t = s?.creationTimeSeconds;
      if (typeof t === "number" && t > latestSec) {
        latestSec = t;
        latest = s;
      }
    }

    const count = submissions.length;

    if (hasOk) {
      const oldestOkMs = oldestOkSec * 1000;
      const onTime = Number.isFinite(deadlineMs) && oldestOkMs <= deadlineMs;

      if (onTime) {
        return {
          kind: "accepted_on_time",
          bg: COLORS.acceptedOnTimeBg,
          lines: [
            formatDateTime(oldestOkMs),
            "OK",
            `${count} submission${count !== 1 ? "s" : ""}`,
          ],
          submissionId: oldestOkSubmission?.id,
          submissionUrl: oldestOkSubmission?.id
            ? `https://codeforces.com/contest/${contestId}/submission/${oldestOkSubmission.id}`
            : null,
        };
      }

      // Accepted exists but is late => shown as "Submitted, not accepted" in blue
      const latestMs = latestSec * 1000;
      const verdict = latest?.verdict ?? "NO_VERDICT";
      return {
        kind: "submitted_with_late_ok",
        bg: COLORS.acceptedLateBg,
        lines: [
          formatDateTime(latestMs),
          String(verdict),
          `${count} submission${count !== 1 ? "s" : ""}`,
        ],
        submissionId: latest?.id,
        submissionUrl: latest?.id
          ? `https://codeforces.com/contest/${contestId}/submission/${latest.id}`
          : null,
      };
    }

    // No OK at all => red
    const latestMs = latestSec * 1000;
    const verdict = latest?.verdict ?? "NO_VERDICT";
    return {
      kind: "submitted_no_ok",
      bg: COLORS.submittedBg,
      lines: [
        formatDateTime(latestMs),
        String(verdict),
        `${count} submission${count !== 1 ? "s" : ""}`,
      ],
      submissionId: latest?.id,
      submissionUrl: latest?.id
        ? `https://codeforces.com/contest/${contestId}/submission/${latest.id}`
        : null,
    };
  }

  let rows = $derived.by(() => {
    const out = [];
    for (const u of PARTICIPANTS) {
      const handle = u.handle;
      const subs = rawByHandle.get(handle) ?? [];
      const byKey = new Map();
      for (const s of subs) {
        const cId = s?.problem?.contestId;
        const idx = s?.problem?.index;
        if (typeof cId !== "number" || typeof idx !== "string") continue;
        const k = problemKey(cId, idx);
        let arr = byKey.get(k);
        if (!arr) {
          arr = [];
          byKey.set(k, arr);
        }
        arr.push(s);
      }

      const cells = [];
      let score = 0;

      for (const p of problemsWithDeadlines) {
        const list = byKey.get(p.key) ?? [];
        const cell = computeCell(list, p.deadlineMs, p.contestId);
        cells.push(cell);
        if (cell.kind === "accepted_on_time") score += 1;
      }

      out.push({
        name: u.name,
        handle: u.handle,
        profileUrl: `https://codeforces.com/profile/${encodeURIComponent(u.handle)}`,
        score,
        cells,
      });
    }

    out.sort((a, b) => {
      if (b.score !== a.score) return b.score - a.score;
      return a.name.localeCompare(b.name);
    });

    // Compute rowspan groups for score column.
    // For each row i, groupSize[i] = n if this row starts group, else 0.
    const groupSize = new Array(out.length).fill(0);
    let i = 0;
    while (i < out.length) {
      let j = i + 1;
      while (j < out.length && out[j].score === out[i].score) j += 1;
      groupSize[i] = j - i;
      i = j;
    }

    return out.map((r, idx) => ({
      ...r,
      scoreRowspan: groupSize[idx],
    }));
  });

  $effect(() => {
    if (fetchedOnce) return;
    fetchedOnce = true;

    (async () => {
      loading = true;
      errorMsg = "";

      try {
        const uniqueHandles = Array.from(
          new Set(
            PARTICIPANTS.map((p) => String(p.handle).trim()).filter(
              (h) => h.length > 0,
            ),
          ),
        );

        const results = await Promise.all(
          uniqueHandles.map(async (h) => {
            const subs = await fetchUserStatus(h);
            return [h, subs];
          }),
        );

        // Create a new Map to trigger reactivity
        const newMap = new Map();
        for (const [h, subs] of results) {
          newMap.set(h, subs);
        }
        rawByHandle = newMap;
      } catch (e) {
        errorMsg = e instanceof Error ? e.message : String(e);
      } finally {
        loading = false;
      }
    })();
  });
</script>

<div class="wrap">
  <div class="title">
    <h1>Scoreboard</h1>
    <div class="meta">
      <div class="tz">Timezone: <b>Europe/Budapest</b></div>
      {#if loading}
        <div class="status">Loading…</div>
      {:else if errorMsg}
        <div class="status error">Error: {errorMsg}</div>
      {:else}
        <div class="status ok">Loaded.</div>
      {/if}
    </div>
  </div>

  <div class="tableWrap">
    <table class="scoreboard">
      <thead>
        <tr>
          <th class="colScore">#</th>
          <th class="colName">Name</th>
          <th class="colHandle">Handle</th>
          {#each problemsWithDeadlines as p}
            <th class="colProblem">
              <div class="ph">
                <a
                  class="plabel"
                  href={p.problemUrl}
                  target="_blank"
                  rel="noreferrer">{p.label}</a
                >
                <a
                  class="psol"
                  href={p.solutionUrl}
                  target="_blank"
                  rel="noreferrer">(sol)</a
                >
              </div>
              <div class="deadline">{p.formattedDeadline}</div>
            </th>
          {/each}
        </tr>
      </thead>

      <tbody>
        {#if rows.length === 0}
          <tr>
            <td class="empty" colspan={3 + problemsWithDeadlines.length}>
              No participants configured.
            </td>
          </tr>
        {:else}
          {#each rows as r, ri}
            <tr>
              {#if r.scoreRowspan > 0}
                <td class="scoreCell" rowspan={r.scoreRowspan}>
                  <div class="scoreVal">{r.score}</div>
                </td>
              {/if}

              <td class="nameCell">{r.name}</td>

              <td class="handleCell">
                <a href={r.profileUrl} target="_blank" rel="noreferrer"
                  >{r.handle}</a
                >
              </td>

              {#each r.cells as c}
                <td class="probCell" style={c.bg ? `background:${c.bg};` : ""}>
                  {#if c.lines.length > 0}
                    {#if c.submissionUrl}
                      <a
                        href={c.submissionUrl}
                        target="_blank"
                        rel="noreferrer"
                        class="cellLink"
                      >
                        <div class="cellText">
                          {#each c.lines as line, li}
                            <div class="line">{line}</div>
                          {/each}
                        </div>
                      </a>
                    {:else}
                      <div class="cellText">
                        {#each c.lines as line, li}
                          <div class="line">{line}</div>
                        {/each}
                      </div>
                    {/if}
                  {/if}
                </td>
              {/each}
            </tr>
          {/each}
        {/if}
      </tbody>
    </table>
  </div>
</div>

<style lang="scss">
  .wrap {
    padding: 16px;
    font-family:
      ui-sans-serif,
      system-ui,
      -apple-system,
      Segoe UI,
      Roboto,
      Helvetica,
      Arial,
      "Apple Color Emoji",
      "Segoe UI Emoji";
  }

  .title {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 12px;

    h1 {
      margin: 0;
      font-size: 20px;
      font-weight: 700;
      letter-spacing: 0.2px;
    }

    .meta {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 12px;

      .status {
        padding: 4px 10px;
        border-radius: 999px;
        background: #f2f2f2;
        color: #333;

        &.ok {
          background: #eef7ee;
          color: #1b5e20;
        }

        &.error {
          background: #fdecec;
          color: #8a1f1f;
        }
      }
    }
  }

  .tableWrap {
    overflow: auto;
    border: 1px solid #e6e6e6;
    border-radius: 10px;
  }

  table.scoreboard {
    border-collapse: collapse;
    width: max-content;
    min-width: 100%;
    background: #fff;

    th,
    td {
      border-bottom: 1px solid #eee;
      border-right: 1px solid #eee;
      padding: 8px 10px;
      vertical-align: top;
    }

    thead th {
      position: sticky;
      top: 0;
      background: #fafafa;
      z-index: 2;
      text-align: left;
      font-size: 12px;
      font-weight: 700;
      color: #222;
    }

    tbody td {
      font-size: 12px;
      color: #111;
    }

    th:last-child,
    td:last-child {
      border-right: none;
    }

    tr:last-child td {
      border-bottom: none;
    }

    .colScore {
      width: 44px;
      min-width: 44px;
      text-align: center;
    }

    .colName {
      min-width: 180px;
    }

    .colHandle {
      min-width: 140px;
    }

    .colProblem {
      min-width: 140px;
    }

    .ph {
      display: flex;
      align-items: baseline;
      gap: 8px;

      .plabel {
        color: #111;
        text-decoration: none;

        &:hover {
          text-decoration: underline;
        }
      }

      .psol {
        font-size: 11px;
        color: #666;
        text-decoration: none;

        &:hover {
          text-decoration: underline;
        }
      }
    }

    .deadline {
      margin-top: 4px;
      font-size: 11px;
      color: #666;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
          "Liberation Mono", "Courier New", monospace;
    }

    .scoreCell {
      text-align: center;
      background: #f8f8f8;

      .scoreVal {
        font-weight: 800;
        font-size: 14px;
        line-height: 1.2;
        padding-top: 2px;
      }
    }

    .handleCell a {
      color: #0b57d0;
      text-decoration: none;

      &:hover {
        text-decoration: underline;
      }
    }

    .probCell {
      white-space: pre-line;
      padding: 0;

      .cellLink {
        display: block;
        text-decoration: none;
        color: inherit;
        transition: opacity 0.15s ease;

        &:hover {
          opacity: 0.85;
          cursor: pointer;
        }
      }

      .cellText {
        padding: 8px 10px;
      }

      .line {
        line-height: 1.2;
        &:not(:last-child) {
          margin-bottom: 2px;
        }
      }
    }

    .empty {
      text-align: center;
      padding: 18px 10px;
      color: #666;
      font-size: 13px;
    }
  }
</style>
