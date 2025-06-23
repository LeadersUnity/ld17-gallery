import React from 'react';
import { Project } from '../types';

interface ProjectCardProps {
  project: Project;
}

const ProjectCard: React.FC<ProjectCardProps> = ({ project }) => {
  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden flex flex-col h-full">
      {project.thumbnail && (
        <div className="h-48 bg-gray-100 flex items-center justify-center overflow-hidden">
          <img 
            src={project.thumbnail} 
            alt={project.projectTitle}
            className="w-full h-full object-cover"
            onError={(e) => {
              e.currentTarget.style.display = 'none';
              e.currentTarget.parentElement!.innerHTML = '<span class="text-6xl">🎮</span>';
            }}
          />
        </div>
      )}
      <div className="p-6 flex flex-col flex-grow">
        <h3 className="text-xl font-bold mb-2">
          {project.projectTitle}
        </h3>
        <p className="text-gray-600 mb-2">{project.studentName}</p>
        {project.description && (
          <p className="text-gray-700 mb-4 flex-grow line-clamp-3">{project.description}</p>
        )}
        <div className="flex flex-col gap-2 mt-auto">
        {project.unityroomUrl && (
          <a
            href={project.unityroomUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="bg-blue-500 text-white text-center py-2 px-4 rounded hover:bg-blue-600 transition-colors"
          >
            unityroomで遊ぶ
          </a>
        )}
        {project.githubReleaseUrl && (
          <a
            href={project.githubReleaseUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="bg-green-500 text-white text-center py-2 px-4 rounded hover:bg-green-600 transition-colors"
          >
            ダウンロード
          </a>
        )}
        <a
          href={project.githubUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="bg-gray-800 text-white text-center py-2 px-4 rounded hover:bg-gray-900 transition-colors"
        >
          GitHub
        </a>
        </div>
      </div>
    </div>
  );
};

export default ProjectCard;