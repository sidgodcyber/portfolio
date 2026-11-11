# Portfolio copy — Siddhi Baluja

The words on the page. Change them here first, then in `index.html`.

### Home
Hi, I'm Siddhi Baluja.
RESEARCH. BUILD. CREATE. REPEAT.
A space-tech enthusiast, interdisciplinary researcher and builder turning
curiosity into real-world solutions.
[Explore My Work] [My Story]

### About Me
A curious mind in an expanding universe.

I'm driven by research that actually solves a problem, and I love bringing ideas
to life at hackathons.

Technology is just a tool. Creativity and out-of-the-box thinking are what will
set us apart in this era of simulated intelligence.

### Areas of Exploration
- Artificial Intelligence: Exploring intelligent systems, machine learning and computer vision.
- Space Technology: Interested in astronomy, space research and technologies that help us understand our universe.
- Robotics & Embedded Systems: Experimenting with hardware, sensors, autonomous systems and edge intelligence.
- Interdisciplinary Research: Connecting ideas across domains to approach complex problems differently.

### Selected Projects (homepage: one line each, full write-ups on projects.html)
- IonWatch (Space Technology · AI/ML · Research): A low-cost station that watches the ionosphere, for space-weather insight. Result: IDE Bootcamp 2026 Winner.
- GNSS Guardian (Autonomous Systems · Computer Vision · IoT): GPS-denied drone navigation that steers by camera when satellite signals fail. Result: SGU HackX 1.0, Second Position, ₹11,000.
- Trishul Net (Earth Sciences · Edge AI · IoT): Early warning for flash floods and debris flows in Uttarakhand's valleys. Status: research prototype.
- Lunar South-Pole Ice Detection (Space Technology · Geospatial · Research): Finding water ice near the lunar south pole with Chandrayaan-2 radar. Built for: Bharatiya Antariksh Hackathon 2026.
- Sand Grain Mapping System (Computer Vision · Edge AI · Earth Sciences): A low-cost camera system that maps and measures sand grains. Result: SIH 2025 Top 5 Finalist.
- Gravity (AI · Systems · Personal Tools): A personal assistant system that remembers my working day.
- Perihelion: The Last Trajectory (Web Game · 3D · Sci-Fi): A cinematic space-survival game, built for a game jam on the theme LOOP. Status: playable in the browser. Play it: https://sidgodcyber.itch.io/perihelion-the-last-trajectory

### Milestones
- 2026, IDE Bootcamp Winner: Winner, Best Performing Team and Pitch Excellence Award for IonWatch.
- 2026, SGU_HACKX 1.0: Second Position among 70 participating teams with GNSS Guardian, and a ₹11,000 cash prize.
- 2026, Research Presentation: Presented my research paper, “Smart Hospitality: Leveraging Artificial Intelligence for Revenue and Yield Management Excellence”, at Avahan 2026, a national conference.

See my certificates (link at the foot of Milestones): https://drive.google.com/drive/folders/1Q37zTbu3zsAgQHEJSoo-k8Fds0UGmAlw
- 2025, Smart India Hackathon: National Finalist, Top 5 teams.
- 2025, Startup Genesis: Second Position and a ₹5,000 cash prize.

### Experience
Software Development Intern, Design Factory India · Noida · June–August 2026 · Paid internship.
Built 10+ interactive museum exhibits where software, interaction design,
computer vision, AI/ML and IoT meet.

Captions: Anatomy Mirror. Your body's organs, moved by hand. / AgeWarp. Your face
at five life stages. The face here is mine. / Scale Explorer. From a 30-metre oak
to a single atom. / The Spawning Window. Coral spawning, set by three dials. /
Interactive mascot. Answers questions out loud, with live lip-sync.

### Beyond Technology
When I'm not building something, you'll probably find me exploring astronomy,
dancing, creating something artistic or getting lost in an interesting idea.

I enjoy communication, storytelling and bringing people together around ideas.

### Contact
LET'S BUILD SOMETHING WORTH BUILDING.
Have an interesting idea, research opportunity or collaboration in mind?
I'd love to hear about it.
GitHub · LinkedIn · Instagram (instagram.com/sidddhiii._) · Résumé (PDF download) · Email
Somewhere between curiosity and the unknown.

---

## Projects page (`projects.html`)

Projects

#### IonWatch (Space Technology · AI/ML · Research)
What it is: An ionospheric scintillation monitoring system designed to provide insights into space weather disturbances. It grew into an incubated startup.

How it works: A low-cost station, a NavIC/GNSS receiver on a Raspberry Pi, watches satellite signals as they pass through the ionosphere. It computes the S4 and phase scintillation indices, the standard measures of how much a signal flickers, through Solar Cycle 25. An offline pipeline turns recorded sessions into per-minute indices, fade events and plots.

- Result: IDE Bootcamp 2026 (AICTE & MoE’s Innovation Cell): Winner, Best Performing Team and Pitch Excellence Award
- Built with: NavIC/GNSS receiver, Raspberry Pi, Python

#### GNSS Guardian (Autonomous Systems · Computer Vision · IoT)
What it is: A GPS-denied drone navigation system that uses optical flow and visual terrain mapping to navigate when satellite signals become unreliable.

How it works: A Raspberry Pi 4 edge module watches the health of every satellite signal: per-satellite signal-strength baselines, fix quality and sudden jumps in position, with a state machine that avoids false alarms. When it detects jamming or spoofing, it falls back to a downward camera to guide the drone home. Optical-flow odometry runs at 30 fps on the Pi, and a camera-versus-GNSS cross-check flags slow spoofs. On hardware, it detected jamming in about two seconds.

- Result: SGU HackX 1.0 (SDGI Global University, Oct 2026): Second Position among 70 teams, ₹11,000 cash prize
- Built with: Raspberry Pi 4, Quectel L86 GNSS, Pi Camera, Python; Shi–Tomasi and Lucas–Kanade tracking, ORB keyframes
- Tested on: A handheld rig carrying the module

#### Trishul Net (Earth Sciences · Edge AI · IoT)
What it is: A low-cost early-warning network for flash floods and debris flows in the side valleys of Uttarakhand.

How it works: Cheap sensor nodes on stable ground beside a stream sample ground vibration at 200 Hz, filter it to 5–45 Hz, and run a trigger and a small on-device classifier. A gateway checks that at least two nodes agree, that the upstream node fired first and that the speed is plausible, which rules out earthquakes. It then estimates the arrival time and sounds the village siren locally, with no internet needed. The models are trained and tested on real public debris-flow recordings from Illgraben, Switzerland.

- Status: Research prototype, not a certified warning system
- Built with: ESP32-S3 sensor nodes and a gateway, Python

#### Lunar South-Pole Ice Detection (Space Technology · Geospatial · Research)
What it is: Water-ice detection and mission planning for crater F2 near the lunar south pole, built for the Bharatiya Antariksh Hackathon 2026.

How it works: A five-stage Python pipeline runs over about 50 GB of NASA LOLA topography (10 m per pixel) and ISRO Chandrayaan-2 DFSAR polarimetric radar. It maps permanently shadowed regions, models illumination, detects ice, picks a landing site and plans a rover traverse. Ice is inferred from the circular polarization ratio, after showing that backscatter inversion can’t tell lunar ice from regolith, and every stage checks itself against published ground truth.

- Findings: Landing Site A at −87.87°S, 82.66°E: 29.3% annual illumination, 5.1° mean slope, 14.6 km from F2. A planned rover traverse of 15.7 km.
- Built with: Python, rasterio, GDAL, NumPy, SciPy

#### Sand Grain Mapping System (Computer Vision · Edge AI · Earth Sciences)
What it is: A low-cost camera-based system for sand grain mapping and analysis, developed for the Smart India Hackathon 2025.

How it works: A Raspberry Pi 5 with a Pi Camera photographs a sample, separates each grain with image processing, and measures the grains with statistical analysis. The whole system sits in a 3D-printed casing.

- Result: Smart India Hackathon 2025: Top 5 Finalist nationwide, Ministry of Earth Sciences
- Built with: Raspberry Pi 5, Pi Camera, 3D-printed casing

#### Gravity (AI · Systems · Personal Tools)
What it is: A personal assistant system that remembers my working day. It records what I do, sorts what I tell it into tasks, notes and client records, and writes me a morning brief.

How it works: A Python system captures git, browser, window and clipboard activity into a portable SQLite brain, and turns natural-language Telegram messages into tasks, notes and client records. Code syncs across my two machines with encryption, while the research trail stays local, behind a firewall that strips out secrets. Search runs over full text and local embeddings, with local Whisper for speech and language models routed under a budget.

- Built with: Python, SQLite, Telegram Bot API, local Whisper, NVIDIA, Gemini and Groq models

#### Perihelion: The Last Trajectory (Web Game · 3D · Sci-Fi)
What it is: A cinematic space-survival game, built for a game jam on the theme LOOP.

How it works: You fly the research spacecraft Kestrel through three hostile sectors, Kestrel Drift, Halcyon Shear and the Shard Belt, managing fuel, hull and engines as you weave through asteroid fields. Lost transmissions piece together what happened to the missions before you, and the signal you follow keeps repeating.

- Status: Playable prototype, in the browser
- Built with: HTML5, in 3D; graphics made with AI assistance
