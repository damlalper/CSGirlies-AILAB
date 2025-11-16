import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import './Theme.css';
import ExperimentVisuals from './ExperimentVisuals';

function App() {
  const [experiments, setExperiments] = useState([]);
  const [selectedExp, setSelectedExp] = useState(null);
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [userInput, setUserInput] = useState('');
  const [currentStep, setCurrentStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [showTutorial, setShowTutorial] = useState(false);
  const [tutorialStep, setTutorialStep] = useState(0);

  const API_URL = 'http://localhost:8000';

  // Check if first time user
  useEffect(() => {
    const hasSeenTutorial = localStorage.getItem('hasSeenTutorial');
    if (!hasSeenTutorial) {
      setShowTutorial(true);
    }
  }, []);

  // Load experiments
  useEffect(() => {
    loadExperiments();
  }, []);

  const loadExperiments = async () => {
    try {
      const res = await axios.get(`${API_URL}/experiments`);
      setExperiments(res.data.experiments);
    } catch (error) {
      console.error('Error loading experiments:', error);
    }
  };

  // Load experiment details
  const loadExperimentDetails = async (expId) => {
    try {
      const res = await axios.get(`${API_URL}/experiments/${expId}`);
      return res.data;
    } catch (error) {
      console.error('Error loading details:', error);
    }
  };

  // Start experiment
  const startExperiment = async (expId) => {
    setLoading(true);
    try {
      const details = await loadExperimentDetails(expId);
      setSelectedExp(details);

      const res = await axios.post(`${API_URL}/simulate/start`, {
        experiment_id: expId,
        level: 'beginner',
        student_name: 'Student'
      });

      setSessionId(res.data.session_id);
      setMessages([
        { sender: 'Partner', text: res.data.partner_message, role: 'partner' },
        { sender: 'System', text: res.data.first_step.title, role: 'system' }
      ]);
      setCurrentStep(1);
      setProgress(0);
    } catch (error) {
      console.error('Error starting experiment:', error);
      alert('Could not start experiment');
    } finally {
      setLoading(false);
    }
  };

  // Send student input
  const sendMessage = async () => {
    if (!userInput.trim()) return;

    const userMsg = { sender: 'You', text: userInput, role: 'user' };
    setMessages([...messages, userMsg]);
    setUserInput('');
    setLoading(true);

    try {
      const res = await axios.post(`${API_URL}/simulate/interact`, {
        session_id: sessionId,
        experiment_id: selectedExp.experiment_id,
        student_message: userInput,
        current_step: currentStep
      });

      setMessages(prev => [
        ...prev,
        { sender: 'Partner', text: res.data.partner_message, role: 'partner' },
        ...(res.data.mentor_guidance ? [{ sender: 'Mentor', text: res.data.mentor_guidance, role: 'mentor' }] : [])
      ]);

      setCurrentStep(res.data.current_step);
      setProgress(res.data.progress);

      if (res.data.wolfram_result) {
        setMessages(prev => [...prev, { 
          sender: 'Graph', 
          image: res.data.wolfram_result.graph_svg, 
          role: 'graph' 
        }]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
    } finally {
      setLoading(false);
    }
  };

  // Complete experiment
  const completeExperiment = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/simulate/complete`, null, {
        params: {
          session_id: sessionId,
          experiment_id: selectedExp.experiment_id
        }
      });

      const gitbookUrl = res.data?.gitbook_response?.gitbook_url;

      if (gitbookUrl) {
        // If a GitBook URL is returned, confirm with the user to open it
        if (window.confirm(`Experiment complete! View the full lab report on GitBook?`)) {
          window.open(gitbookUrl, '_blank');
        }
      } else {
        // Fallback message if no URL is present
        alert(res.data.message || "Experiment completed successfully!");
      }

      resetApp();
    } catch (error) {
      console.error('Error completing experiment:', error);
      alert('Could not complete the experiment. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const resetApp = () => {
    setSelectedExp(null);
    setSessionId(null);
    setMessages([]);
    setCurrentStep(1);
    setProgress(0);
  };

  // Export report
  const exportReport = async (format) => {
    if (!sessionId || !selectedExp) return;

    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/export/report`, null, {
        params: {
          session_id: sessionId,
          experiment_id: selectedExp.experiment_id,
          format: format
        }
      });

      if (res.data.success) {
        alert(`Report exported successfully as ${format.toUpperCase()}!\nFile: ${res.data.file_path || 'Multiple files'}`);
      }
    } catch (error) {
      console.error('Error exporting report:', error);
      alert('Could not export report. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Tutorial functions
  const tutorialSteps = [
    {
      title: "Welcome to CSGirlies-AILAB! 🧪",
      content: "Your AI-powered virtual lab partner that makes science education accessible anywhere, anytime."
    },
    {
      title: "Meet Your AI Lab Partner 🤖",
      content: "Alex is your curious lab companion who will guide you through experiments, ask proactive questions, and help you discover scientific concepts."
    },
    {
      title: "How It Works 💬",
      content: "Simply chat with your AI partner! Type your observations, ask questions, and respond naturally. The AI remembers your conversation and adapts to your learning pace."
    },
    {
      title: "Get Real-Time Computations 📊",
      content: "Powered by Wolfram Alpha, you'll see dynamic graphs, calculations, and scientific visualizations based on your experiment data."
    },
    {
      title: "Ready to Start? 🚀",
      content: "Select an experiment, start chatting with your AI partner, and experience science like never before!"
    }
  ];

  const nextTutorialStep = () => {
    if (tutorialStep < tutorialSteps.length - 1) {
      setTutorialStep(tutorialStep + 1);
    } else {
      closeTutorial();
    }
  };

  const prevTutorialStep = () => {
    if (tutorialStep > 0) {
      setTutorialStep(tutorialStep - 1);
    }
  };

  const closeTutorial = () => {
    setShowTutorial(false);
    localStorage.setItem('hasSeenTutorial', 'true');
  };

  const skipTutorial = () => {
    closeTutorial();
  };

  return (
    <div className="App">
      <header className="header">
        <h1>🧪 CSGirlies-AILAB</h1>
        <p>Interactive Experiment Environment Powered by AI</p>
        <button
          onClick={() => setShowTutorial(true)}
          className="btn-tutorial"
          title="View Tutorial"
        >
          ❓ Help
        </button>
      </header>

      {/* Onboarding Tutorial Modal */}
      {showTutorial && (
        <div className="tutorial-overlay">
          <div className="tutorial-modal">
            <div className="tutorial-header">
              <h2>{tutorialSteps[tutorialStep].title}</h2>
              <button onClick={skipTutorial} className="btn-close">✕</button>
            </div>

            <div className="tutorial-content">
              <div className="tutorial-icon">
                {tutorialStep === 0 && "🧪"}
                {tutorialStep === 1 && "🤖"}
                {tutorialStep === 2 && "💬"}
                {tutorialStep === 3 && "📊"}
                {tutorialStep === 4 && "🚀"}
              </div>
              <p>{tutorialSteps[tutorialStep].content}</p>
            </div>

            <div className="tutorial-footer">
              <div className="tutorial-dots">
                {tutorialSteps.map((_, idx) => (
                  <span
                    key={idx}
                    className={`dot ${idx === tutorialStep ? 'active' : ''}`}
                  />
                ))}
              </div>

              <div className="tutorial-buttons">
                {tutorialStep > 0 && (
                  <button onClick={prevTutorialStep} className="btn-secondary">
                    ← Back
                  </button>
                )}
                <button onClick={skipTutorial} className="btn-secondary">
                  Skip
                </button>
                <button onClick={nextTutorialStep} className="btn-primary">
                  {tutorialStep === tutorialSteps.length - 1 ? "Get Started!" : "Next →"}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {!selectedExp ? (
        // Experiment Selection Screen
        <div className="experiments-container">
          <h2>Select Available Experiments</h2>
          <div className="experiments-grid">
            {experiments.map(exp => (
              <div key={exp.id} className="experiment-card">
                <h3>{exp.title}</h3>
                <p className="subject">{exp.subject}</p>
                <p className="duration"><i className="fas fa-clock"></i> {exp.duration_minutes} minutes</p>
                <p className="description">{exp.description}</p>
                <button 
                  onClick={() => startExperiment(exp.id)}
                  className="btn-start"
                >
                  <i className="fas fa-rocket"></i> Start
                </button>
              </div>
            ))}
          </div>
        </div>
      ) : (
        // Experiment Workspace Screen
        <div className="experiment-workspace">
          <div className="experiment-header">
            <h2>{selectedExp.title}</h2>
            <div className="progress-bar">
              <div className="progress-fill" style={{ width: `${progress}%` }}>
                {Math.round(progress)}%
              </div>
            </div>
          </div>

          <div className="experiment-content">
            <div className="chat-container">
              {/* Experiment Visualization */}
              <ExperimentVisuals
                experimentId={selectedExp.experiment_id}
                currentStep={currentStep}
                progress={progress}
              />

              <div className="messages">
                {messages.map((msg, idx) => (
                  <div key={idx} className={`message ${msg.role}`}>
                    <strong><i className={`fas fa-${msg.role === 'user' ? 'user-astronaut' : 'robot'}`}></i> {msg.sender}:</strong>
                    {msg.image ? (
                      <img src={`data:image/svg+xml;base64,${msg.image}`} alt="Graph" />
                    ) : (
                      <p>{msg.text}</p>
                    )}
                  </div>
                ))}
                {loading && <div className="message system"><em>Waiting for response...</em></div>}
              </div>

              <div className="input-area">
                <input
                  type="text"
                  value={userInput}
                  onChange={(e) => setUserInput(e.target.value)}
                  onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                  placeholder="Write your answer..."
                  disabled={loading}
                />
                <button 
                  onClick={sendMessage}
                  disabled={loading}
                  className="btn-send"
                >
                  <i className="fas fa-paper-plane"></i> Send
                </button>
              </div>
            </div>

            <div className="sidebar">
              <h3><i className="fas fa-info-circle"></i> Experiment Information</h3>
              <div className="info-box">
                <h4>Step {currentStep}</h4>
                <p><strong>Subject:</strong> {selectedExp.subject}</p>
                <p><strong>Level:</strong> {selectedExp.level}</p>
              </div>

              <div className="info-box">
                <h4><i className="fas fa-bullseye"></i> Learning Objectives</h4>
                <ul>
                  {selectedExp.learning_objectives.slice(0, 3).map((obj, idx) => (
                    <li key={idx}>{obj}</li>
                  ))}
                </ul>
              </div>

              <div className="info-box">
                <h4><i className="fas fa-download"></i> Export Report</h4>
                <div style={{ display: 'flex', gap: '5px', flexWrap: 'wrap' }}>
                  <button
                    onClick={() => exportReport('pdf')}
                    className="btn-export"
                    disabled={loading}
                    title="Export as PDF"
                  >
                    PDF
                  </button>
                  <button
                    onClick={() => exportReport('markdown')}
                    className="btn-export"
                    disabled={loading}
                    title="Export as Markdown"
                  >
                    MD
                  </button>
                  <button
                    onClick={() => exportReport('csv')}
                    className="btn-export"
                    disabled={loading}
                    title="Export as CSV"
                  >
                    CSV
                  </button>
                  <button
                    onClick={() => exportReport('json')}
                    className="btn-export"
                    disabled={loading}
                    title="Export as JSON"
                  >
                    JSON
                  </button>
                </div>
              </div>

              <button
                onClick={completeExperiment}
                className="btn-complete"
                disabled={loading}
              >
                <i className="fas fa-check-circle"></i> Complete Experiment
              </button>
              <button
                onClick={resetApp}
                className="btn-cancel"
              >
                <i className="fas fa-times-circle"></i> Change Experiment
              </button>
            </div>
          </div>
        </div>
      )}

      <footer className="footer">
        <p>CSGirlies Team © 2025 - Making Education Accessible <i className="fas fa-heart" style={{color: 'var(--primary)'}}></i></p>
      </footer>
    </div>
  );
}

export default App;