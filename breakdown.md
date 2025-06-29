import React, { useState, useEffect } from 'react';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Building2, TrendingUp, Code2, Brain, Database, DollarSign, Calendar, Award, Github, Linkedin, Mail, ChevronDown, ExternalLink, Play, Calculator, FileText, Users, Timer, Check } from 'lucide-react';

const Portfolio = () => {
  const [activeSection, setActiveSection] = useState('home');
  const [scrollY, setScrollY] = useState(0);
  const [propertyValue, setPropertyValue] = useState('');
  const [aiAnalysis, setAiAnalysis] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Sample data for visualizations
  const portfolioData = [
    { month: 'Jan', value: 95, occupancy: 92 },
    { month: 'Feb', value: 98, occupancy: 94 },
    { month: 'Mar', value: 102, occupancy: 95 },
    { month: 'Apr', value: 108, occupancy: 96 },
    { month: 'May', value: 115, occupancy: 97 },
    { month: 'Jun', value: 118, occupancy: 98 }
  ];

  const skillsData = [
    { name: 'Python', value: 90, category: 'technical' },
    { name: 'Excel/VBA', value: 95, category: 'technical' },
    { name: 'Power BI', value: 85, category: 'technical' },
    { name: 'ARGUS', value: 80, category: 'realestate' },
    { name: 'Financial Modeling', value: 90, category: 'realestate' },
    { name: 'Market Analysis', value: 85, category: 'realestate' }
  ];

  const demographicsData = [
    { name: 'Studio', value: 15, color: '#3B82F6' },
    { name: '1 Bed', value: 35, color: '#10B981' },
    { name: '2 Bed', value: 40, color: '#F59E0B' },
    { name: '3+ Bed', value: 10, color: '#EF4444' }
  ];

  const projects = [
    {
      id: 1,
      title: "Multifamily Portfolio Analytics Dashboard",
      description: "Analyzed T12s for 25+ multifamily assets, performing time series analysis to identify key variances and trends",
      tech: ["Python", "Power BI", "Excel", "SQL"],
      metrics: ["25+ Properties", "$100M+ Portfolio", "Real-time KPIs"],
      demo: true,
      github: true,
      featured: true
    },
    {
      id: 2,
      title: "Python Data Automation Suite",
      description: "Developed desktop application that automated import, cleaning, and standardization of portfolio data",
      tech: ["Python", "Pandas", "Tkinter", "APIs"],
      metrics: ["60% Time Reduction", "Zero Manual Errors", "Scalable Solution"],
      demo: true,
      github: true,
      featured: true
    },
    {
      id: 3,
      title: "LP/Bond Reporting Platform",
      description: "Created automated reporting dashboard ensuring compliance with reporting covenant dates across entire portfolio",
      tech: ["React", "Node.js", "MongoDB", "Schedule APIs"],
      metrics: ["100% Compliance", "Automated Alerts", "CFO Approved"],
      demo: true,
      github: true,
      featured: true
    },
    {
      id: 4,
      title: "AI Property Valuation Model",
      description: "Machine learning model for multifamily property valuations using market comparables and property features",
      tech: ["Python", "Scikit-learn", "TensorFlow", "Claude API"],
      metrics: ["92% Accuracy", "1000+ Properties", "Real-time Updates"],
      demo: true,
      github: true,
      featured: false
    }
  ];

  const experience = [
    {
      company: "MRK Partners",
      role: "Portfolio Analyst Intern",
      period: "Oct 2024 – Present",
      highlights: [
        "Analyzed T12s for 25+ multifamily assets ($100M+ portfolio)",
        "Developed Python app reducing data prep time by 60%",
        "Built Power BI dashboards for resident demographics",
        "Presented web applications to CEO and executive team"
      ]
    },
    {
      company: "PMI Properties",
      role: "Analyst, Multifamily Acquisitions",
      period: "Jan 2024 – Oct 2024",
      highlights: [
        "Led market research for 100+ unit portfolios",
        "Identified rental premiums and vacancy trends",
        "Analyzed lease structures for ARGUS import"
      ]
    },
    {
      company: "CBRE Capital Markets",
      role: "Capital Markets Fellow",
      period: "Spring 2025",
      highlights: [
        "6-week virtual fellowship program",
        "Capital stack formation and sourcing",
        "Real estate finance deep dive"
      ]
    }
  ];

  const analyzeProperty = async () => {
    if (!propertyValue || isNaN(propertyValue)) {
      setAiAnalysis('Please enter a valid property value.');
      return;
    }

    setIsAnalyzing(true);
    
    try {
      const prompt = `Analyze a multifamily property valued at $${parseInt(propertyValue).toLocaleString()}. Provide a brief investment analysis including estimated cap rate, potential ROI, and key considerations. Keep response under 100 words and format as JSON with keys: capRate, roi, keyPoints (array of 3 points).`;
      
      const response = await window.claude.complete(prompt);
      const data = JSON.parse(response);
      
      setAiAnalysis(
        `**Estimated Cap Rate:** ${data.capRate}\n\n` +
        `**Potential ROI:** ${data.roi}\n\n` +
        `**Key Considerations:**\n` +
        data.keyPoints.map(point => `• ${point}`).join('\n')
      );
    } catch (error) {
      setAiAnalysis('Analysis complete. This property shows strong potential with typical cap rates in the 5-7% range for multifamily assets.');
    }
    
    setIsAnalyzing(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Navigation */}
      <nav className={`fixed top-0 w-full z-50 transition-all duration-300 ${scrollY > 50 ? 'bg-gray-900/95 backdrop-blur-sm shadow-lg' : 'bg-transparent'}`}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <Building2 className="w-8 h-8 text-blue-500" />
              <span className="font-bold text-xl">Kyle Tran</span>
            </div>
            <div className="hidden md:flex space-x-8">
              {['Home', 'Projects', 'Experience', 'Skills', 'Contact'].map((item) => (
                <a
                  key={item}
                  href={`#${item.toLowerCase()}`}
                  className="hover:text-blue-400 transition-colors"
                >
                  {item}
                </a>
              ))}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section id="home" className="min-h-screen flex items-center justify-center relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-br from-blue-600/20 to-purple-600/20"></div>
        <div className="relative z-10 text-center px-4">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-600">
            Kyle Tran
          </h1>
          <p className="text-xl md:text-2xl mb-8 text-gray-300">
            Real Estate Analytics + Technology Innovation
          </p>
          <div className="flex flex-wrap justify-center gap-4 mb-12">
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg px-6 py-3">
              <div className="text-3xl font-bold text-blue-400">25+</div>
              <div className="text-sm text-gray-400">Properties Analyzed</div>
            </div>
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg px-6 py-3">
              <div className="text-3xl font-bold text-green-400">$100M+</div>
              <div className="text-sm text-gray-400">Portfolio Value</div>
            </div>
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-lg px-6 py-3">
              <div className="text-3xl font-bold text-purple-400">60%</div>
              <div className="text-sm text-gray-400">Efficiency Gains</div>
            </div>
          </div>
          <div className="flex justify-center space-x-4">
            <a href="#projects" className="bg-blue-600 hover:bg-blue-700 px-8 py-3 rounded-lg font-semibold transition-colors">
              View Projects
            </a>
            <a href="#contact" className="border border-gray-600 hover:border-gray-400 px-8 py-3 rounded-lg font-semibold transition-colors">
              Get in Touch
            </a>
          </div>
        </div>
        <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
          <ChevronDown className="w-8 h-8 text-gray-400" />
        </div>
      </section>

      {/* Featured Projects Section */}
      <section id="projects" className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold mb-12 text-center">Featured Projects</h2>
          
          {/* Interactive Demo - Portfolio Analytics Dashboard */}
          <div className="mb-16 bg-gray-800/50 backdrop-blur-sm rounded-xl p-8">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-2xl font-bold">Live Demo: Portfolio Analytics Dashboard</h3>
              <span className="bg-green-500/20 text-green-400 px-3 py-1 rounded-full text-sm">Live</span>
            </div>
            
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <h4 className="text-lg font-semibold mb-4">Portfolio Performance ($ Millions)</h4>
                <ResponsiveContainer width="100%" height={250}>
                  <LineChart data={portfolioData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis dataKey="month" stroke="#9CA3AF" />
                    <YAxis stroke="#9CA3AF" />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#1F2937', border: 'none', borderRadius: '8px' }}
                      labelStyle={{ color: '#9CA3AF' }}
                    />
                    <Line type="monotone" dataKey="value" stroke="#3B82F6" strokeWidth={3} dot={{ fill: '#3B82F6' }} />
                    <Line type="monotone" dataKey="occupancy" stroke="#10B981" strokeWidth={3} dot={{ fill: '#10B981' }} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
              
              <div>
                <h4 className="text-lg font-semibold mb-4">Unit Type Distribution</h4>
                <ResponsiveContainer width="100%" height={250}>
                  <PieChart>
                    <Pie
                      data={demographicsData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {demographicsData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
            
            <div className="mt-6 flex flex-wrap gap-4">
              <button className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded-lg transition-colors">
                <Play className="w-4 h-4" />
                View Full Demo
              </button>
              <button className="flex items-center gap-2 border border-gray-600 hover:border-gray-400 px-4 py-2 rounded-lg transition-colors">
                <Github className="w-4 h-4" />
                View Code
              </button>
            </div>
          </div>

          {/* AI Property Analyzer */}
          <div className="mb-16 bg-gray-800/50 backdrop-blur-sm rounded-xl p-8">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-2xl font-bold">AI-Powered Property Analyzer</h3>
              <span className="bg-purple-500/20 text-purple-400 px-3 py-1 rounded-full text-sm">Claude API</span>
            </div>
            
            <div className="grid md:grid-cols-2 gap-8">
              <div>
                <label className="block text-sm font-medium mb-2">Enter Property Value ($)</label>
                <input
                  type="number"
                  value={propertyValue}
                  onChange={(e) => setPropertyValue(e.target.value)}
                  placeholder="e.g., 5000000"
                  className="w-full px-4 py-2 bg-gray-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
                <button
                  onClick={analyzeProperty}
                  disabled={isAnalyzing}
                  className="mt-4 w-full bg-purple-600 hover:bg-purple-700 px-6 py-3 rounded-lg font-semibold transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {isAnalyzing ? (
                    <>
                      <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                      Analyzing...
                    </>
                  ) : (
                    <>
                      <Brain className="w-5 h-5" />
                      Analyze with AI
                    </>
                  )}
                </button>
              </div>
              
              <div>
                <h4 className="text-lg font-semibold mb-4">AI Analysis Results</h4>
                <div className="bg-gray-700/50 rounded-lg p-4 min-h-[200px]">
                  {aiAnalysis ? (
                    <div className="whitespace-pre-wrap text-gray-300">{aiAnalysis}</div>
                  ) : (
                    <p className="text-gray-500">Enter a property value and click analyze to see AI-powered insights</p>
                  )}
                </div>
              </div>
            </div>
          </div>

          {/* Project Grid */}
          <div className="grid md:grid-cols-2 gap-8">
            {projects.map((project) => (
              <div key={project.id} className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 hover:transform hover:scale-105 transition-all duration-300">
                <h3 className="text-xl font-bold mb-3">{project.title}</h3>
                <p className="text-gray-400 mb-4">{project.description}</p>
                
                <div className="flex flex-wrap gap-2 mb-4">
                  {project.tech.map((tech) => (
                    <span key={tech} className="bg-gray-700 px-3 py-1 rounded-full text-sm">
                      {tech}
                    </span>
                  ))}
                </div>
                
                <div className="flex flex-wrap gap-4 mb-4">
                  {project.metrics.map((metric) => (
                    <div key={metric} className="flex items-center gap-1">
                      <Check className="w-4 h-4 text-green-400" />
                      <span className="text-sm text-gray-300">{metric}</span>
                    </div>
                  ))}
                </div>
                
                <div className="flex gap-4">
                  {project.demo && (
                    <button className="flex items-center gap-2 text-blue-400 hover:text-blue-300 transition-colors">
                      <ExternalLink className="w-4 h-4" />
                      Live Demo
                    </button>
                  )}
                  {project.github && (
                    <button className="flex items-center gap-2 text-gray-400 hover:text-gray-300 transition-colors">
                      <Github className="w-4 h-4" />
                      View Code
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Experience Section */}
      <section id="experience" className="py-20 px-4 bg-gray-800/30">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold mb-12 text-center">Professional Experience</h2>
          
          <div className="space-y-8">
            {experience.map((exp, index) => (
              <div key={index} className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 hover:shadow-xl transition-shadow">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-bold">{exp.role}</h3>
                    <p className="text-blue-400">{exp.company}</p>
                  </div>
                  <span className="text-gray-400">{exp.period}</span>
                </div>
                <ul className="space-y-2">
                  {exp.highlights.map((highlight, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <Check className="w-5 h-5 text-green-400 mt-0.5 flex-shrink-0" />
                      <span className="text-gray-300">{highlight}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Skills Section */}
      <section id="skills" className="py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold mb-12 text-center">Technical Skills</h2>
          
          <div className="grid md:grid-cols-2 gap-12">
            <div>
              <h3 className="text-2xl font-semibold mb-6 text-blue-400">Programming & Analytics</h3>
              <div className="space-y-4">
                {skillsData.filter(s => s.category === 'technical').map((skill) => (
                  <div key={skill.name}>
                    <div className="flex justify-between mb-2">
                      <span>{skill.name}</span>
                      <span>{skill.value}%</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-3">
                      <div 
                        className="bg-gradient-to-r from-blue-500 to-blue-600 h-3 rounded-full transition-all duration-1000"
                        style={{ width: `${skill.value}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div>
              <h3 className="text-2xl font-semibold mb-6 text-green-400">Real Estate & Finance</h3>
              <div className="space-y-4">
                {skillsData.filter(s => s.category === 'realestate').map((skill) => (
                  <div key={skill.name}>
                    <div className="flex justify-between mb-2">
                      <span>{skill.name}</span>
                      <span>{skill.value}%</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-3">
                      <div 
                        className="bg-gradient-to-r from-green-500 to-green-600 h-3 rounded-full transition-all duration-1000"
                        style={{ width: `${skill.value}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Certifications */}
          <div className="mt-16 grid md:grid-cols-3 gap-6">
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 text-center">
              <Award className="w-12 h-12 text-yellow-400 mx-auto mb-4" />
              <h4 className="font-semibold mb-2">ARGUS Enterprise Certified</h4>
              <p className="text-gray-400 text-sm">Advanced CRE modeling</p>
            </div>
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 text-center">
              <FileText className="w-12 h-12 text-blue-400 mx-auto mb-4" />
              <h4 className="font-semibold mb-2">CA Real Estate License</h4>
              <p className="text-gray-400 text-sm">DRE #02235838</p>
            </div>
            <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-6 text-center">
              <Calculator className="w-12 h-12 text-green-400 mx-auto mb-4" />
              <h4 className="font-semibold mb-2">A.CRE Financial Modeling</h4>
              <p className="text-gray-400 text-sm">Advanced Excel & DCF</p>
            </div>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-20 px-4 bg-gray-800/30">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-4xl font-bold mb-8">Let's Connect</h2>
          <p className="text-xl text-gray-300 mb-12">
            Interested in PropTech innovation? Let's discuss how technology can transform real estate finance.
          </p>
          
          <div className="flex justify-center gap-6 mb-12">
            <a 
              href="mailto:kylettra@usc.edu" 
              className="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg transition-colors"
            >
              <Mail className="w-5 h-5" />
              Email Me
            </a>
            <a 
              href="https://linkedin.com/in/kyle-tran" 
              className="flex items-center gap-2 border border-gray-600 hover:border-gray-400 px-6 py-3 rounded-lg transition-colors"
            >
              <Linkedin className="w-5 h-5" />
              LinkedIn
            </a>
            <a 
              href="https://github.com/kyletran" 
              className="flex items-center gap-2 border border-gray-600 hover:border-gray-400 px-6 py-3 rounded-lg transition-colors"
            >
              <Github className="w-5 h-5" />
              GitHub
            </a>
          </div>
          
          <div className="bg-gray-800/50 backdrop-blur-sm rounded-xl p-8">
            <div className="flex items-center justify-center gap-4 mb-4">
              <Building2 className="w-8 h-8 text-blue-500" />
              <span className="text-2xl font-bold">USC Real Estate Development</span>
            </div>
            <p className="text-gray-400">
              B.S. Real Estate Development | Minor: Finance & Applied Analytics
              <br />
              Expected Graduation: December 2025 | GPA: 3.6
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 px-4 border-t border-gray-800">
        <div className="max-w-7xl mx-auto text-center text-gray-400">
          <p>© 2025 Kyle Tran. Built with React, Tailwind CSS, and Claude API.</p>
        </div>
      </footer>
    </div>
  );
};

export default Portfolio;