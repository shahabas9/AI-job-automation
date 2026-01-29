import React, { useState, useEffect } from 'react';
import { X, Copy, Download, Bot, ExternalLink, Loader2, Check, FileText } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { prepareApplication, assistApply } from '../services/api';
import clsx from 'clsx';

const ApplicationModal = ({ job, profile, onClose }) => {
    const [step, setStep] = useState('generating'); // generating, review, assist
    const [resume, setResume] = useState('');
    const [coverLetter, setCoverLetter] = useState('');
    const [assistData, setAssistData] = useState(null);
    const [error, setError] = useState(null);
    const [copiedRes, setCopiedRes] = useState(false);
    const [copiedCL, setCopiedCL] = useState(false);

    useEffect(() => {
        let mounted = true;

        const generate = async () => {
            try {
                const data = await prepareApplication(profile, job);
                if (mounted) {
                    setResume(data.resume_text);
                    setCoverLetter(data.cover_letter_text);
                    setStep('review');
                }
            } catch (err) {
                if (mounted) setError('Failed to generate application materials.');
            }
        };

        if (step === 'generating') {
            generate();
        }

        return () => { mounted = false; };
    }, [profile, job, step]);

    const handleCopy = (text, setCopied) => {
        navigator.clipboard.writeText(text);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    const handleDownload = (filename, text) => {
        const element = document.createElement("a");
        const file = new Blob([text], { type: 'text/plain' });
        element.href = URL.createObjectURL(file);
        element.download = filename;
        document.body.appendChild(element);
        element.click();
        document.body.removeChild(element);
    };

    const handleAssist = async () => {
        try {
            const data = await assistApply(job);
            setAssistData(data);
            setStep('assist');
        } catch (err) {
            setError('Failed to start assisted application.');
        }
    };

    // URL Fix included here
    const applyUrl = job.job.apply_url || job.job.redirect_url || job.job.job_apply_link || job.job.url || '#';

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-white rounded-2xl shadow-xl w-full max-w-5xl max-h-[90vh] flex flex-col overflow-hidden"
            >
                {/* Header */}
                <div className="px-6 py-4 border-b border-gray-100 flex justify-between items-center bg-gray-50">
                    <div>
                        <h2 className="text-lg font-bold text-gray-900">
                            {step === 'generating' ? 'Preparing Application...' :
                                step === 'assist' ? 'Assisted Application' :
                                    'Review Application Package'}
                        </h2>
                        <p className="text-sm text-gray-500">{job.job.job_title} @ {job.job.company_name}</p>
                    </div>
                    <button onClick={onClose} className="p-2 hover:bg-gray-200 rounded-full transition-colors">
                        <X size={20} />
                    </button>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto p-6 bg-gray-50/50">
                    {error ? (
                        <div className="text-center py-12 text-red-600">
                            <p>{error}</p>
                            <button
                                onClick={onClose}
                                className="mt-4 px-4 py-2 bg-gray-200 rounded-lg hover:bg-gray-300"
                            >
                                Close
                            </button>
                        </div>
                    ) : step === 'generating' ? (
                        <div className="flex flex-col items-center justify-center h-full py-20">
                            <Loader2 size={48} className="animate-spin text-primary-500 mb-4" />
                            <p className="text-lg font-medium text-gray-700">Tailoring your resume...</p>
                            <p className="text-gray-500 mt-2">Our AI is analyzing the job requirements.</p>
                        </div>
                    ) : step === 'assist' ? (
                        <div className="max-w-2xl mx-auto py-8">
                            <div className="bg-blue-50 border border-blue-200 rounded-xl p-6 mb-8 text-blue-800">
                                <h3 className="font-bold flex items-center gap-2 mb-2">
                                    <Bot size={20} />
                                    Assisted Application Mode
                                </h3>
                                <p className="mb-2">{assistData?.warning || "You must manually submit the application."}</p>
                            </div>

                            <div className="space-y-6">
                                <h4 className="font-semibold text-gray-900 border-b pb-2">Instructions</h4>
                                <ol className="list-decimal list-inside space-y-3 text-gray-700">
                                    {assistData?.instructions?.map((inst, i) => (
                                        <li key={i}>{inst}</li>
                                    ))}
                                </ol>

                                <div className="pt-6 flex gap-4">
                                    <a
                                        href={assistData?.apply_url}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="flex-1 bg-primary-600 hover:bg-primary-700 text-white py-3 rounded-xl font-bold text-center flex items-center justify-center gap-2"
                                    >
                                        Open Job Application <ExternalLink size={18} />
                                    </a>
                                    <button
                                        onClick={() => setStep('review')}
                                        className="flex-1 bg-white border border-gray-300 text-gray-700 py-3 rounded-xl font-medium hover:bg-gray-50"
                                    >
                                        Back to Docs
                                    </button>
                                </div>
                            </div>
                        </div>
                    ) : (
                        <div className="grid md:grid-cols-2 gap-6 h-full">
                            {/* Resume Column */}
                            <div className="flex flex-col h-full">
                                <div className="flex justify-between items-center mb-2 px-1">
                                    <label className="font-semibold text-gray-700 flex items-center gap-2">
                                        <FileText size={16} /> Tailored Resume
                                    </label>
                                    <div className="flex gap-2">
                                        <button
                                            onClick={() => handleCopy(resume, setCopiedRes)}
                                            className="p-1.5 text-gray-500 hover:text-primary-600 hover:bg-primary-50 rounded transition-colors"
                                            title="Copy"
                                        >
                                            {copiedRes ? <Check size={16} /> : <Copy size={16} />}
                                        </button>
                                        <button
                                            onClick={() => handleDownload('tailored_resume.txt', resume)}
                                            className="p-1.5 text-gray-500 hover:text-primary-600 hover:bg-primary-50 rounded transition-colors"
                                            title="Download"
                                        >
                                            <Download size={16} />
                                        </button>
                                    </div>
                                </div>
                                <textarea
                                    value={resume}
                                    onChange={(e) => setResume(e.target.value)}
                                    className="flex-1 w-full p-4 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none font-mono text-sm bg-white shadow-sm"
                                    placeholder="Resume content..."
                                />
                            </div>

                            {/* Cover Letter Column */}
                            <div className="flex flex-col h-full">
                                <div className="flex justify-between items-center mb-2 px-1">
                                    <label className="font-semibold text-gray-700 flex items-center gap-2">
                                        <FileText size={16} /> Cover Letter
                                    </label>
                                    <div className="flex gap-2">
                                        <button
                                            onClick={() => handleCopy(coverLetter, setCopiedCL)}
                                            className="p-1.5 text-gray-500 hover:text-primary-600 hover:bg-primary-50 rounded transition-colors"
                                            title="Copy"
                                        >
                                            {copiedCL ? <Check size={16} /> : <Copy size={16} />}
                                        </button>
                                        <button
                                            onClick={() => handleDownload('cover_letter.txt', coverLetter)}
                                            className="p-1.5 text-gray-500 hover:text-primary-600 hover:bg-primary-50 rounded transition-colors"
                                            title="Download"
                                        >
                                            <Download size={16} />
                                        </button>
                                    </div>
                                </div>
                                <textarea
                                    value={coverLetter}
                                    onChange={(e) => setCoverLetter(e.target.value)}
                                    className="flex-1 w-full p-4 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none font-mono text-sm bg-white shadow-sm"
                                    placeholder="Cover letter content..."
                                />
                            </div>
                        </div>
                    )}
                </div>

                {/* Footer Actions */}
                {step === 'review' && (
                    <div className="p-4 border-t border-gray-100 bg-white flex justify-end gap-3">
                        <button
                            onClick={handleAssist}
                            className="px-6 py-2.5 border border-primary-200 text-primary-700 hover:bg-primary-50 rounded-lg font-medium flex items-center gap-2 transition-colors"
                        >
                            <Bot size={18} />
                            Assist Me Applying
                        </button>
                        <a
                            href={applyUrl}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="px-6 py-2.5 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-bold flex items-center gap-2 transition-colors shadow-lg shadow-primary-200"
                        >
                            Apply on Site <ExternalLink size={18} />
                        </a>
                    </div>
                )}
            </motion.div>
        </div>
    );
};

export default ApplicationModal;
