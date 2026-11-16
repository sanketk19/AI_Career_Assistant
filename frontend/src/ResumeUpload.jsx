
import { useRef, useState } from 'react'

function ResumeUpload({
  onAnalysisSuccess,
  onJobsReceived,
  onCandidateReceived
}) {
  const fileInputRef = useRef(null)

  const [message, setMessage] = useState('')
  const [analysis, setAnalysis] = useState('')
  const [loading, setLoading] = useState(false)

  const handleFileChange = async (event) => {
    const selectedFile = event.target.files[0]

    if (!selectedFile) return

    setAnalysis('')

    if (selectedFile.type !== 'application/pdf') {
      setMessage('Please select a PDF file.')
      event.target.value = ''
      return
    }

    if (selectedFile.size > 5 * 1024 * 1024) {
      setMessage('File size must be less than 5 MB.')
      event.target.value = ''
      return
    }

    const formData = new FormData()
    formData.append('resume', selectedFile)

    try {
      setLoading(true)
      setMessage('Analyzing resume and searching jobs...')

      const response = await fetch(
        'http://127.0.0.1:8000/api/ai/resume-analysis/',
        {
          method: 'POST',
          body: formData,
        }
      )

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Resume analysis failed')
      }

      // Resume Analysis
      setAnalysis(data.analysis || '')

      // AI Recommended Job Roles
      const recommendedJobs = Array.isArray(data.recommended_jobs)
        ? data.recommended_jobs
        : []

      // Actual Job Search Results
      const availableJobs = Array.isArray(data.available_jobs)
        ? data.available_jobs
        : []

      // Send both job lists to App.jsx
      onJobsReceived(recommendedJobs, availableJobs)

      // Candidate Details
      const candidate = {
        candidate_type: data.candidate_type || 'Unknown',
        total_experience_years: data.total_experience_years ?? 0,
        internship_experience_months:
          data.internship_experience_months ?? 0,
        skills: Array.isArray(data.skills) ? data.skills : [],
        education: data.education || 'Not Available'
      }

      onCandidateReceived(candidate)

      // Resume Status
      onAnalysisSuccess(selectedFile.name)

      if (data.job_search_error) {
        setMessage(
          'Resume analyzed, but job search failed: ' +
          data.job_search_error
        )
      } else {
        setMessage(
          `Resume analyzed successfully! ${availableJobs.length} jobs found.`
        )
      }

    } catch (error) {
      setMessage('Error: ' + error.message)
    } finally {
      setLoading(false)
      event.target.value = ''
    }
  }

  return (
    <div className="card">
      <h3>AI Resume Analysis</h3>

      <input
        type="file"
        accept=".pdf,application/pdf"
        ref={fileInputRef}
        onChange={handleFileChange}
        style={{ display: 'none' }}
      />

      <button
        onClick={() => fileInputRef.current.click()}
        disabled={loading}
      >
        {loading ? 'Analyzing...' : 'Upload Resume'}
      </button>

      {message && <p>{message}</p>}

      {analysis && (
        <div className="analysis-result">
          <h3>Resume Analysis Result</h3>

          <pre
            style={{
              whiteSpace: 'pre-wrap',
              fontFamily: 'inherit'
            }}
          >
            {analysis}
          </pre>
        </div>
      )}
    </div>
  )
}

export default ResumeUpload
