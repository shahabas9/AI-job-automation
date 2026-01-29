import React, { useState } from 'react';
import { MapPin, Building, ChevronDown, ChevronUp, ExternalLink, FileText, Bot, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import clsx from 'clsx';
import ReactMarkdown from 'react-markdown';

const JobCard = ({ job, onPrepare, onAssist }) => {
    const [isExpanded, setIsExpanded] = useState(false);
    const { final_score, job: jobData } = job;

    // Format score as percentage
    const matchPercentage = Math.round((final_score || 0) * 100);

    // Determine color based on score
    const scoreColor = matchPercentage >= 80 ? 'text-green-600 bg-green-50' :
        matchPercentage >= 60 ? 'text-yellow-600 bg-yellow-50' :
            'text-orange-600 bg-orange-50';

    const progressColor = matchPercentage >= 80 ? 'bg-green-500' :
        matchPercentage >= 60 ? 'bg-yellow-500' :
            'bg-orange-500';

    const applyUrl = jobData.apply_url || jobData.redirect_url || jobData.job_apply_link || jobData.url || '#';

    return (
        <motion.div
            layout
            className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden hover:shadow-md transition-shadow"
        >
            <div className="p-6">
                <div className="flex justify-between items-start gap-4">
                    <div className="flex-1">
                        <h3 className="text-xl font-bold text-gray-900 mb-1">{jobData.job_title || jobData.title || "Unknown Title"}</h3>
                        <div className="flex items-center gap-4 text-sm text-gray-500 mb-3">
                            <div className="flex items-center gap-1">
                                <Building size={16} />
                                <span>{jobData.company_name || jobData.company || "Unknown Company"}</span>
                            </div>
                            <div className="flex items-center gap-1">
                                <MapPin size={16} />
                                <span>{jobData.location || "Remote"}</span>
                            </div>
                        </div>
                    </div>

                    <div className="flex flex-col items-end min-w-[80px]">
                        <div className={clsx("px-3 py-1 rounded-full font-bold text-sm mb-2", scoreColor)}>
                            {matchPercentage}% Match
                        </div>
                        {/* Match explanation tooltip could go here */}
                    </div>
                </div>

                {/* Score Bar */}
                <div className="w-full h-1.5 bg-gray-100 rounded-full mb-6 overflow-hidden">
                    <div
                        className={clsx("h-full rounded-full transition-all duration-1000 ease-out", progressColor)}
                        style={{ width: `${matchPercentage}%` }}
                    />
                </div>

                <div className="flex flex-wrap gap-3">
                    <button
                        onClick={() => onPrepare(job)}
                        className="flex-1 min-w-[160px] bg-primary-600 hover:bg-primary-700 text-white px-4 py-2.5 rounded-lg font-medium flex items-center justify-center gap-2 transition-colors"
                    >
                        <Sparkles size={18} />
                        Prepare Application
                    </button>

                    <div className="flex gap-2 flex-1 min-w-[200px]">
                        <a
                            href={applyUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2.5 rounded-lg font-medium flex items-center justify-center gap-2 transition-colors"
                        >
                            Apply Now
                            <ExternalLink size={16} />
                        </a>

                        <button
                            onClick={() => onAssist(job)}
                            className="px-4 py-2.5 border border-primary-200 text-primary-700 hover:bg-primary-50 rounded-lg font-medium flex items-center justify-center gap-2 transition-colors"
                            title="Assisted Apply"
                        >
                            <Bot size={18} />
                            <span className="hidden sm:inline">Assist Me</span>
                        </button>
                    </div>
                </div>

                <button
                    onClick={() => setIsExpanded(!isExpanded)}
                    className="w-full mt-4 flex items-center justify-center gap-1 text-sm text-gray-500 hover:text-gray-700 pt-2 border-t border-gray-50 transition-colors"
                >
                    {isExpanded ? (
                        <>Less Details <ChevronUp size={16} /></>
                    ) : (
                        <>View Details <ChevronDown size={16} /></>
                    )}
                </button>
            </div>

            <AnimatePresence>
                {isExpanded && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: 'auto', opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        className="bg-gray-50 border-t border-gray-100"
                    >
                        <div className="p-6 prose prose-sm max-w-none text-gray-600">
                            <h4 className="text-sm font-semibold text-gray-900 mb-2">Job Description</h4>
                            <div className="line-clamp-[20]">
                                {jobData.job_description || jobData.description ?
                                    (jobData.job_description || jobData.description).split('\n').map((line, i) => (
                                        <p key={i} className="mb-2">{line}</p>
                                    )) :
                                    <p className="italic text-gray-400">No description available.</p>
                                }
                            </div>

                            {job.explanation && (
                                <div className="mt-4 bg-primary-50 p-4 rounded-lg border border-primary-100">
                                    <h4 className="text-sm font-semibold text-primary-900 mb-1 flex items-center gap-2">
                                        <Sparkles size={14} />
                                        Why it's a match
                                    </h4>
                                    <p className="text-primary-800">{job.explanation}</p>
                                </div>
                            )}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </motion.div>
    );
};

export default JobCard;
