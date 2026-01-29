import React, { useState, useEffect } from 'react';
import ResumeUpload from './components/ResumeUpload';
import JobList from './components/JobList';
import ApplicationModal from './components/ApplicationModal';
import { fetchJobs, assistApply } from './services/api';

function App() {
  const [profile, setProfile] = useState(null);
  const [jobs, setJobs] = useState([]);
  const [pagination, setPagination] = useState({ page: 1, size: 20, total: 0 });
  const [isLoadingJobs, setIsLoadingJobs] = useState(false);
  const [selectedJob, setSelectedJob] = useState(null);

  const loadJobs = async (currProfile, page = 1) => {
    if (!currProfile) return;

    setIsLoadingJobs(true);
    try {
      const data = await fetchJobs(currProfile, page);
      setJobs(data.jobs);
      setPagination({
        page: data.page,
        size: data.size,
        total: data.total
      });
    } catch (err) {
      console.error("Failed to load jobs", err);
    } finally {
      setIsLoadingJobs(false);
    }
  };

  const handleProfileExtracted = (extractedProfile) => {
    setProfile(extractedProfile);
    loadJobs(extractedProfile, 1);
  };

  const handlePageChange = (newPage) => {
    loadJobs(profile, newPage);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handlePrepare = (job) => {
    setSelectedJob(job);
  };

  const handleAssist = (job) => {
    setSelectedJob(job);
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans">
      <header className="bg-white border-b border-gray-100 sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="bg-primary-600 text-white p-2 rounded-lg font-bold">AI</div>
            <h1 className="text-xl font-bold tracking-tight text-gray-900">Job Hunter</h1>
          </div>
          {profile && (
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-500 hidden sm:inline">
                User: {profile.primary_role}
              </span>
              <button
                onClick={() => { setProfile(null); setJobs([]); }}
                className="text-sm text-primary-600 hover:text-primary-700 font-medium"
              >
                Upload New Resume
              </button>
            </div>
          )}
        </div>
      </header>

      <main>
        {!profile ? (
          <div className="pt-10 pb-20 px-4">
            <div className="text-center max-w-2xl mx-auto mb-10">
              <h1 className="text-4xl font-extrabold text-gray-900 mb-4 tracking-tight">
                Find Your Dream Job with <span className="text-primary-600">AI Precision</span>
              </h1>
              <p className="text-lg text-gray-600">
                Upload your resume and let our AI agents match you with the best opportunities,
                tailor your application, and assist you in applying.
              </p>
            </div>
            <ResumeUpload onProfileExtracted={handleProfileExtracted} />
          </div>
        ) : (
          <JobList
            jobs={jobs}
            page={pagination.page}
            total={pagination.total}
            size={pagination.size}
            onPageChange={handlePageChange}
            onPrepare={handlePrepare}
            onAssist={handleAssist}
            isLoading={isLoadingJobs}
          />
        )}
      </main>

      {selectedJob && (
        <ApplicationModal
          job={selectedJob}
          profile={profile}
          onClose={() => setSelectedJob(null)}
        />
      )}
    </div>
  );
}

export default App;
