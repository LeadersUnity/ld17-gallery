import { useState, useMemo } from 'react';
import SearchBar from './components/SearchBar';
import ProjectList from './components/ProjectList';
import { projects } from './data/projects';

function App() {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredProjects = useMemo(() => {
    if (!searchTerm) return projects;

    const lowerSearchTerm = searchTerm.toLowerCase();
    return projects.filter((project) => {
      return (
        project.projectTitle.toLowerCase().includes(lowerSearchTerm) ||
        project.studentName.toLowerCase().includes(lowerSearchTerm) ||
        project.description.toLowerCase().includes(lowerSearchTerm)
      );
    });
  }, [searchTerm]);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800">
            17期Unity作品集
          </h1>
        </header>

        <SearchBar searchTerm={searchTerm} onSearchChange={setSearchTerm} />

        <div className="mb-6 text-center">
          <p className="text-gray-600">
            表示中: {filteredProjects.length} / {projects.length} 作品
          </p>
        </div>

        <ProjectList projects={filteredProjects} />
      </div>
    </div>
  );
}

export default App