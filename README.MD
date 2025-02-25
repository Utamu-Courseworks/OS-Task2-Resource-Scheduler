# CSC 2101 - OPERATING SYSTEMS | TASK 2

## Resource Scheduler Project

### Project Overview
This project involves designing and implementing a **Resource Scheduler** to optimize the allocation of employees (bank tellers or call center agents) to customer requests. The system aims to:
- Minimize customer wait times.
- Maximize resource utilization.
- Ensure fairness in task distribution.

---

## Project Tasks & Deliverables

### Activity 1: Project Setup
- Form teams of **2–3 students**.
- Create a **GitHub repository** for the project.
- All team members must contribute and collaborate through individual GitHub profiles.
- Set up a **GitHub Project Board** to manage tasks and milestones.

**Deliverable:** GitHub repository with initial setup and team members added.

---

### Activity 2: System Design & Implementation
The system simulates the arrival of customers in a bank, each with:
- **Randomized service time**.
- **Priority level** (VIP, Corporate, or Normal).

#### Features:
- **Dynamic Agent Assignment:**
  - Bank tellers or call center agents are assigned based on **availability** and **workload capacity**.
  - Each agent has a **workload limit** and an **availability status** (busy/free).
- **Scheduling Algorithms Implemented:**
  - **Round Robin Scheduling** – Each agent receives tasks equally.
  - **Priority Scheduling** – VIP and Corporate customers are served first.
  - **Shortest Job Next** – Tasks with shorter service times are prioritized.
- **Real-Time Monitoring:**
  - Agent availability and workload status updates **every 5 seconds**.
  - Enables **bank managers** to make informed staffing decisions.
- **Performance Metrics:**
  - **Average customer waiting time**.
  - **Agent utilization rate** (working vs. idle time).
  - **Fairness in task distribution**.

---

### Activity 3: Containerization & CI/CD Pipeline
#### Containerization with Docker
- **Write a Dockerfile** to containerize the application.
- Ensure the application can run in a **containerized environment**.

#### CI/CD with GitHub Actions
- **Set up GitHub Actions** for automating testing and deployment.
- Configure CI/CD pipeline to:
  - **Build and test** the application on every commit.
  - **Push Docker images** to Docker Hub.
  - **Deploy the application** to a cloud platform (GitHub Pages, AWS, etc.).

**Deliverable:** Deployed application URL.

---

## Project Repository Structure
```
📂 resource-scheduler
 ├── 📂 src               # Source code
 ├── 📂 docs              # Documentation (SRS, Reports, etc.)
 ├── 📂 tests             # Unit and Integration Tests
 ├── 📂 docker            # Docker configuration files
 ├── .github/workflows    # CI/CD GitHub Actions workflows
 ├── Dockerfile           # Docker container setup
 ├── README.md            # Project overview and guidelines
 ├── requirements.txt     # Dependencies (if using Python)
 ├── package.json         # Dependencies (if using JavaScript/Node.js)
 └── LICENSE              # License information
```

---

## Installation & Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-team/resource-scheduler.git
   cd resource-scheduler
   ```
2. **Run the application locally:**
   ```bash
   # If using Python
   python main.py
   ```
   ```bash
   # If using Node.js
   npm install
   npm start
   ```
3. **Run in Docker:**
   ```bash
   docker build -t resource-scheduler .
   docker run -p 8000:8000 resource-scheduler
   ```

---

## Contribution Guidelines
- Follow **GitHub Flow**: Fork → Clone → Branch → Commit → Pull Request.
- Write **clear commit messages**.
- Keep PRs **small and focused**.
- Run tests before submitting a PR.

---

## Marking Scheme
| Criteria | Description |
|----------|-------------|
| **SRS Document** | Updated and detailed Software Requirements Specification. |
| **GitHub Repository** | Developed code + documentation available. |
| **Final Presentation** | Showcase project functionality. |
| **Individual Contributions** | Tracked via GitHub commits & pull requests. |
| **CI/CD Pipeline Setup** | GitHub Actions + Automated Deployment. |

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Contact
For any queries, contact **your-team-email@example.com** or create an issue in the GitHub repository.

Happy Coding! 🚀
