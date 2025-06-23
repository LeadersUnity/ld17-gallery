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
        project.description.toLowerCase().includes(lowerSearchTerm) ||
        (project.tags && project.tags.some((tag) => tag.toLowerCase().includes(lowerSearchTerm)))
      );
    });
  }, [searchTerm]);

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            研修生Unity作品ギャラリー
          </h1>
          <p className="text-lg text-gray-600">
            研修生が制作したUnityゲームの作品集です
          </p>
        </header>

        <SearchBar searchTerm={searchTerm} onSearchChange={setSearchTerm} />

        <div className="mb-4">
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