import React from 'react';
import { ChevronLeft, ChevronRight, Loader2 } from 'lucide-react';
import JobCard from './JobCard';

const JobList = ({ jobs, page, total, size, onPageChange, onPrepare, onAssist, isLoading }) => {
    const totalPages = Math.ceil(total / size);

    if (isLoading) {
        return (
            <div className="flex flex-col items-center justify-center py-20 text-gray-500">
                <Loader2 size={40} className="animate-spin mb-4 text-primary-500" />
                <p>Finding the best jobs for you...</p>
            </div>
        );
    }

    if (jobs.length === 0) {
        return (
            <div className="text-center py-20 text-gray-500">
                <p>No jobs found. Try adjusting your profile matches.</p>
            </div>
        );
    }

    return (
        <div className="max-w-6xl mx-auto p-4 sm:p-6 pb-20">
            <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-gray-800">Top Job Matches</h2>
                <span className="text-gray-500 text-sm">Found {total} jobs</span>
            </div>

            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-2">
                {jobs.map((job, index) => (
                    <JobCard
                        key={job.job?.job_id || index}
                        job={job}
                        onPrepare={onPrepare}
                        onAssist={onAssist}
                    />
                ))}
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
                <div className="flex justify-center items-center gap-4 mt-10">
                    <button
                        onClick={() => onPageChange(page - 1)}
                        disabled={page <= 1}
                        className="p-2 border rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        <ChevronLeft size={20} />
                    </button>

                    <span className="text-sm font-medium text-gray-600">
                        Page {page} of {totalPages}
                    </span>

                    <button
                        onClick={() => onPageChange(page + 1)}
                        disabled={page >= totalPages}
                        className="p-2 border rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        <ChevronRight size={20} />
                    </button>
                </div>
            )}
        </div>
    );
};

export default JobList;
