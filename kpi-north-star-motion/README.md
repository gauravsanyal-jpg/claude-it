# KPI Dashboard — North Star · Motion Graphic

A 76-second animated explainer (1080×1350, 4:5) of the *Prompting 101 — KPI Dashboard North Star* carousel.

- `kpi-north-star.mp4`: rendered video, 30 fps, ready for LinkedIn or Instagram
- `index.html`: the animation source. Open it in a browser to play it (space = play/pause, slider to scrub)
- `render.js`: re-renders the MP4 (`node render.js 30 out.mp4`; needs Playwright + ffmpeg)

| Time | Scene |
|---|---|
| 0–7s | Hook: "If a metric does not trigger a decision, it is decoration." |
| 7–16s | 40 metric tiles pop in, refresh weekly, then go grey: "Reviewed by nobody." |
| 16–26s | One rule: each tile is checked for a decision, 40 → 8 survivors regroup with their decisions |
| 26–37s | North Star diagram builds; signals flow from the inputs → North Star → lagging outcomes |
| 37–59s | The two-part prompt types out |
| 59–67s | What you get back: a live decision dashboard with thresholds (one red alarm triggers a decision) |
| 67–76s | CTA and author card |
