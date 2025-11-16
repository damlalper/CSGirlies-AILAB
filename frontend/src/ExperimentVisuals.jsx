import React, { useState, useEffect } from 'react';
import './ExperimentVisuals.css';

const ExperimentVisuals = ({ experimentId, currentStep, progress }) => {
  const [animationState, setAnimationState] = useState('initial');

  useEffect(() => {
    // Update animation based on progress
    if (experimentId === 'acid_base_titration') {
      if (progress < 30) setAnimationState('clear');
      else if (progress < 70) setAnimationState('lightPink');
      else setAnimationState('pink');
    } else if (experimentId === 'hookes_law') {
      // Spring animation based on progress
      setAnimationState(`stretch${Math.min(Math.floor(progress / 20), 5)}`);
    } else if (experimentId === 'osmosis') {
      // Water movement animation
      setAnimationState(`osmosis${Math.min(Math.floor(progress / 25), 4)}`);
    }
  }, [experimentId, progress]);

  if (experimentId === 'acid_base_titration') {
    return (
      <div className="visual-container">
        <div className="titration-visual">
          <div className="burette">
            <div className="burette-liquid" style={{ height: `${100 - progress}%` }}>
              <span className="burette-label">NaOH</span>
            </div>
          </div>
          <div className="flask">
            <div className={`flask-liquid ${animationState}`}>
              <div className="bubbles">
                {progress > 50 && (
                  <>
                    <div className="bubble" style={{ left: '20%', animationDelay: '0s' }}></div>
                    <div className="bubble" style={{ left: '50%', animationDelay: '0.5s' }}></div>
                    <div className="bubble" style={{ left: '70%', animationDelay: '1s' }}></div>
                  </>
                )}
              </div>
            </div>
            <div className="flask-label">HCl + Indicator</div>
          </div>
          <div className="color-indicator">
            <div className="indicator-label">pH Indicator Color:</div>
            <div className={`color-box ${animationState}`}></div>
            <div className="ph-value">
              {animationState === 'clear' && 'pH ~2 (Acidic)'}
              {animationState === 'lightPink' && 'pH ~6 (Neutralizing)'}
              {animationState === 'pink' && 'pH ~9 (Basic)'}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (experimentId === 'hookes_law') {
    const springStretch = Math.min(progress, 100);
    return (
      <div className="visual-container">
        <div className="spring-visual">
          <div className="ceiling"></div>
          <div className="spring" style={{ height: `${100 + springStretch}px` }}>
            {[...Array(15)].map((_, i) => (
              <div key={i} className="spring-coil"></div>
            ))}
          </div>
          <div className="weight" style={{ top: `${100 + springStretch}px` }}>
            <div className="weight-label">{Math.round(progress * 0.5)}g</div>
          </div>
          <div className="displacement-indicator">
            <div className="arrow-down"></div>
            <div className="displacement-value">Δx = {springStretch.toFixed(1)} cm</div>
          </div>
        </div>
      </div>
    );
  }

  if (experimentId === 'osmosis') {
    return (
      <div className="visual-container">
        <div className="osmosis-visual">
          <div className="beaker beaker-left">
            <div className="solution hypotonic">
              <div className="water-molecules">
                {[...Array(8)].map((_, i) => (
                  <div
                    key={i}
                    className={`molecule ${progress > 30 ? 'moving-right' : ''}`}
                    style={{
                      top: `${20 + i * 10}%`,
                      left: `${10 + (i % 3) * 25}%`,
                      animationDelay: `${i * 0.2}s`
                    }}
                  >
                    H₂O
                  </div>
                ))}
              </div>
            </div>
            <div className="beaker-label">Hypotonic Solution</div>
          </div>

          <div className="membrane">
            <div className="membrane-line"></div>
            <div className="membrane-label">Semi-permeable Membrane</div>
            {progress > 20 && (
              <div className="arrows">
                <div className="arrow-right">→</div>
                <div className="arrow-left" style={{ opacity: 0.3 }}>←</div>
              </div>
            )}
          </div>

          <div className="beaker beaker-right">
            <div className="solution hypertonic" style={{ height: `${50 + progress * 0.3}%` }}>
              <div className="solute-particles">
                {[...Array(12)].map((_, i) => (
                  <div
                    key={i}
                    className="particle"
                    style={{
                      top: `${10 + i * 8}%`,
                      left: `${15 + (i % 4) * 20}%`
                    }}
                  >
                    •
                  </div>
                ))}
              </div>
            </div>
            <div className="beaker-label">Hypertonic Solution</div>
          </div>

          <div className="osmosis-info">
            <div className="info-text">
              Water Flow: {progress < 30 ? 'Starting...' : progress < 70 ? 'Active →' : 'Equilibrating'}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return null;
};

export default ExperimentVisuals;
