
import { useState } from 'react'
import './App.css'
import ResumeUpload from './ResumeUpload'
import Chatbot from './Chatbot.jsx'

function App() {
  const [activePage, setActivePage] = useState('Dashboard')
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  const [resumeName, setResumeName] = useState('')
  const [recommendedJobs, setRecommendedJobs] = useState([])
  const [availableJobs, setAvailableJobs] = useState([])
  const [candidateInfo, setCandidateInfo] = useState(null)

  const [careerRoadmap, setCareerRoadmap] = useState(null)
  const [roadmapLoading, setRoadmapLoading] = useState(false)
  const [roadmapError, setRoadmapError] = useState('')

  const handleAnalysisSuccess = (fileName) => {
    setResumeName(fileName)
    setCareerRoadmap(null)
    setRoadmapError('')
  }

  const handleJobsReceived = (recommended, available) => {
    setRecommendedJobs(recommended || [])
    setAvailableJobs(available || [])
  }

  const handleCandidateReceived = (candidate) => {
    setCandidateInfo(candidate)
    setCareerRoadmap(null)
    setRoadmapError('')
  }

  // Format Job Description into bullet points
  const getDescriptionPoints = (description) => {
    if (!description) return []

    const headings = [
      'Job Title',
      'Company',
      'Location',
      'Job Type',
      'Internship Duration',
      'Stipend',
      'Experience',
      'About the Role',
      'Key Responsibilities',
      'Responsibilities',
      'Skills and Qualifications',
      'Required Skills',
      'Qualifications',
      'Requirements'
    ]

    let text = String(description)
      .replace(/\r/g, '')
      .replace(/\s+/g, ' ')
      .trim()

    const headingPattern = new RegExp(
      `\\s*(?=\\b(?:${headings.join('|')})\\s*:)`,
      'gi'
    )

    text = text.replace(headingPattern, '\n')
    text = text.replace(/([.!?])(?=[A-Z])/g, '$1\n')

    return text
      .split('\n')
      .flatMap(section => section.split(/(?<=[.!?])\s+/))
      .map(point => point.trim())
      .filter(point => point.length > 2)
  }

  // Generate AI Career Roadmap
  const generateRoadmap = async () => {
    if (!candidateInfo || !candidateInfo.skills?.length) {
      setRoadmapError('Please upload your resume first.')
      return
    }

    setRoadmapLoading(true)
    setRoadmapError('')
    setCareerRoadmap(null)

    try {
      const response = await fetch(
        'http://127.0.0.1:8000/api/ai/career-roadmap/',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            candidate_info: candidateInfo
          })
        }
      )

      const data = await response.json()

      if (!response.ok || !data.success) {
        throw new Error(
          data.error || 'Failed to generate career roadmap'
        )
      }

      setCareerRoadmap(data.roadmap)

    } catch (error) {
      setRoadmapError(error.message || 'Something went wrong.')
    } finally {
      setRoadmapLoading(false)
    }
  }

  const averageMatch = recommendedJobs.length > 0
    ? Math.round(
        recommendedJobs.reduce(
          (total, job) =>
            total + (Number(job.match_percentage) || 0),
          0
        ) / recommendedJobs.length
      )
    : 0

  const menuItems = [
    'Dashboard',
    'My Resume',
    'Find Jobs',
    'Job Matching',
    'AI Career Roadmap',
    'AI Chatbot'
  ]

  // Dashboard
  const renderDashboard = () => (
    <>
      <section className="welcome">
        <h2>Welcome to Your Career Dashboard</h2>
        <p>Build your career with AI-powered assistance.</p>
      </section>

      <section className="cards">
        <div className="card">
          <h3>Resume Status</h3>
          <h2>{resumeName ? 'Uploaded' : 'Not Uploaded'}</h2>
          <p>{resumeName || 'Upload your PDF resume'}</p>
        </div>

        <div className="card">
          <h3>Candidate Type</h3>
          <h2>{candidateInfo?.candidate_type || 'Not Available'}</h2>
          <p>Based on resume analysis</p>
        </div>

        <div className="card">
          <h3>Work Experience</h3>
          <h2>
            {candidateInfo
              ? `${candidateInfo.total_experience_years} Years`
              : 'Not Available'}
          </h2>
          <p>Full-time experience</p>
        </div>

        <div className="card">
          <h3>Recommended Jobs</h3>
          <h2>{recommendedJobs.length}</h2>
          <p>AI suggested job roles</p>
        </div>

        <div className="card">
          <h3>Available Jobs</h3>
          <h2>{availableJobs.length}</h2>
          <p>Google Jobs search results</p>
        </div>

        <div className="card">
          <h3>Skill Match</h3>
          <h2>{averageMatch}%</h2>
          <p>Average AI job match</p>
        </div>
      </section>

      <section className="card">
        <h3>Candidate Profile</h3>

        {candidateInfo ? (
          <>
            <p><strong>Education:</strong> {candidateInfo.education}</p>
            <p>
              <strong>Skills:</strong>{' '}
              {candidateInfo.skills.join(', ')}
            </p>
            <p>
              <strong>Internship Experience:</strong>{' '}
              {candidateInfo.internship_experience_months} Months
            </p>
          </>
        ) : (
          <p>Upload your resume to see your profile.</p>
        )}
      </section>
    </>
  )

  // Resume Page
  const renderResume = () => (
    <>
      <h2>My Resume</h2>
      <p>Upload your resume and get AI-powered analysis.</p>

      <ResumeUpload
        onAnalysisSuccess={handleAnalysisSuccess}
        onJobsReceived={handleJobsReceived}
        onCandidateReceived={handleCandidateReceived}
      />

      <section className="card">
        <h3>Resume Information</h3>

        <p>
          <strong>Resume:</strong>{' '}
          {resumeName || 'No resume uploaded'}
        </p>

        {candidateInfo && (
          <>
            <p>
              <strong>Candidate Type:</strong>{' '}
              {candidateInfo.candidate_type}
            </p>

            <p>
              <strong>Education:</strong>{' '}
              {candidateInfo.education}
            </p>

            <p>
              <strong>Experience:</strong>{' '}
              {candidateInfo.total_experience_years} Years
            </p>

            <p>
              <strong>Internship:</strong>{' '}
              {candidateInfo.internship_experience_months} Months
            </p>

            <p>
              <strong>Technical Skills:</strong>{' '}
              {candidateInfo.skills.join(', ')}
            </p>
          </>
        )}
      </section>
    </>
  )

  // Find Jobs Page
  const renderAvailableJobs = () => (
    <>
      <div className="jobs-heading">
        <div>
          <h2>Latest Job Opportunities</h2>
          <p>Jobs discovered based on your resume skills.</p>
        </div>

        <div className="job-count">
          {availableJobs.length} Jobs Found
        </div>
      </div>

      {availableJobs.length === 0 ? (
        <section className="card">
          <h3>No Jobs Found</h3>
          <p>Upload your resume first to find matching jobs.</p>
        </section>
      ) : (
        <div className="jobs-container">
          {availableJobs.map((job, index) => (
            <div
              className="card job-item"
              key={job.job_id || index}
            >
              <div className="job-top">
                <div>
                  <h3>{job.job_title}</h3>
                  <h4>{job.company_name}</h4>
                </div>

                <span className="job-number">
                  Job #{index + 1}
                </span>
              </div>

              <div className="job-details">
                <div>
                  <strong>Location</strong>
                  <p>{job.location || 'Not Available'}</p>
                </div>

                <div>
                  <strong>Experience</strong>
                  <p>{job.experience_required || 'Not Available'}</p>
                </div>

                <div>
                  <strong>Posted</strong>
                  <p>{job.posted_at || 'Not Available'}</p>
                </div>
              </div>

              <div className="job-skills">
                <strong>Matching Skills</strong>

                <div className="skill-tags">
                  {Array.isArray(job.matching_skills) &&
                  job.matching_skills.length > 0 ? (
                    job.matching_skills.map((skill, skillIndex) => (
                      <span key={skillIndex}>{skill}</span>
                    ))
                  ) : (
                    <p>No matching skills found</p>
                  )}
                </div>
              </div>

              <div className="job-description">
                <strong>Job Description</strong>

                {job.description ? (
                  <ul>
                    {getDescriptionPoints(job.description).map(
                      (point, pointIndex) => (
                        <li key={pointIndex}>{point}</li>
                      )
                    )}
                  </ul>
                ) : (
                  <p>Description not available</p>
                )}
              </div>

              <div className="job-footer">
                <span>{job.source}</span>

                {job.apply_url ? (
                  <a
                    href={job.apply_url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Apply Now ↗
                  </a>
                ) : job.job_url ? (
                  <a
                    href={job.job_url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    View Job ↗
                  </a>
                ) : (
                  <span>Application link unavailable</span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </>
  )

  // AI Job Matching Page
  const renderJobMatching = () => (
    <>
      <h2>AI Job Matching</h2>
      <p>Job roles recommended by AI based on your resume.</p>

      {recommendedJobs.length === 0 ? (
        <section className="card">
          <p>Upload your resume to get AI job recommendations.</p>
        </section>
      ) : (
        recommendedJobs.map((job, index) => (
          <div className="card job-item" key={index}>
            <h3>{job.title}</h3>

            <p>
              <strong>Match:</strong> {job.match_percentage}%
            </p>

            <p>
              <strong>Required Skills:</strong>{' '}
              {Array.isArray(job.required_skills)
                ? job.required_skills.join(', ')
                : 'Not Available'}
            </p>

            <p>
              <strong>Experience Required:</strong>{' '}
              {job.experience_required || 'Not Available'}
            </p>

            <p>
              <strong>Reason:</strong>{' '}
              {job.reason || 'Not Available'}
            </p>
          </div>
        ))
      )}
    </>
  )

  // AI Career Roadmap Page
  const renderCareerRoadmap = () => (
    <>
      <section className="card">
        <h2>AI Career Roadmap</h2>
        <p>
          Generate a personalized learning roadmap based on your resume.
        </p>

        {!candidateInfo && (
          <p>
            Please upload your resume from the My Resume page first.
          </p>
        )}

        <button
          onClick={generateRoadmap}
          disabled={!candidateInfo || roadmapLoading}
        >
          {roadmapLoading
            ? 'Generating Roadmap...'
            : 'Generate Career Roadmap'}
        </button>

        {roadmapError && (
          <p style={{ color: 'red', marginTop: '15px' }}>
            {roadmapError}
          </p>
        )}
      </section>

      {careerRoadmap && (
        <>
          <section className="card">
            <h2>{careerRoadmap.career_goal}</h2>

            <p>
              <strong>Current Level:</strong>{' '}
              {careerRoadmap.current_level}
            </p>

            <p>
              <strong>Estimated Timeline:</strong>{' '}
              {careerRoadmap.estimated_timeline}
            </p>
          </section>

          <section className="card">
            <h3>Current Skills</h3>
            <div className="skill-tags">
              {careerRoadmap.current_skills?.map((skill, index) => (
                <span key={index}>{skill}</span>
              ))}
            </div>
          </section>

          <section className="card">
            <h3>Skills to Learn</h3>
            <div className="skill-tags">
              {careerRoadmap.skills_to_learn?.map((skill, index) => (
                <span key={index}>{skill}</span>
              ))}
            </div>
          </section>

          <section className="card">
            <h3>Step-by-Step Learning Roadmap</h3>

            {careerRoadmap.roadmap?.map((phase, index) => (
              <div className="card job-item" key={index}>
                <h3>{phase.phase}: {phase.title}</h3>

                <p>
                  <strong>Duration:</strong> {phase.duration}
                </p>

                <p><strong>Topics to Learn:</strong></p>

                <ul>
                  {phase.topics?.map((topic, topicIndex) => (
                    <li key={topicIndex}>{topic}</li>
                  ))}
                </ul>

                <p>
                  <strong>Practical Project:</strong>{' '}
                  {phase.project}
                </p>
              </div>
            ))}
          </section>

          <section className="card">
            <h3>Recommended Projects</h3>

            <ul>
              {careerRoadmap.recommended_projects?.map(
                (project, index) => (
                  <li key={index}>{project}</li>
                )
              )}
            </ul>
          </section>
        </>
      )}
    </>
  )

  // Page Navigation
  const renderPage = () => {
    switch (activePage) {
      case 'Dashboard':
        return renderDashboard()

      case 'My Resume':
        return renderResume()

      case 'Find Jobs':
        return renderAvailableJobs()

      case 'Job Matching':
        return renderJobMatching()

      case 'AI Career Roadmap':
        return renderCareerRoadmap()

      case 'AI Chatbot':
        return (
          <Chatbot
            candidateInfo={candidateInfo}
            careerRoadmap={careerRoadmap}
          />
        )

      default:
        return renderDashboard()
    }
  }

  return (
    <div className={isMenuOpen ? 'app menu-open' : 'app'}>

      <aside className="sidebar">
        <h2>CareerAI</h2>

        <nav>
          {menuItems.map((item) => (
            <button
              key={item}
              className={
                activePage === item
                  ? 'nav-button active'
                  : 'nav-button'
              }
              onClick={() => {
                setActivePage(item)
                setIsMenuOpen(false)
              }}
            >
              {item}
            </button>
          ))}
        </nav>
      </aside>

      <main className="main-content">
        <header>
          <button
            className="mobile-menu-btn"
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            aria-label="Toggle navigation menu"
          >
            {isMenuOpen ? '✕' : '☰'}
          </button>

          <div>
            <h1>AI Career Assistant</h1>
            <p>{activePage}</p>
          </div>
        </header>

        {renderPage()}
      </main>
    </div>
  )
}

export default App
