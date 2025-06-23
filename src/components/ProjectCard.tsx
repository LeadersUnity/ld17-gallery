import React from 'react';
import { Project } from '../types';

interface ProjectCardProps {
  project: Project;
}

const ProjectCard: React.FC<ProjectCardProps> = ({ project }) => {
  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 p-6 flex flex-col h-full">
      <h3 className="text-xl font-bold mb-2">{project.projectTitle}</h3>
      <p className="text-gray-600 mb-2">制作者: {project.studentName}</p>
      <p className="text-gray-700 mb-4 flex-grow">{project.description}</p>
      {project.tags && project.tags.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          {project.tags.map((tag, index) => (
            <span
              key={index}
              className="px-2 py-1 bg-blue-100 text-blue-700 text-sm rounded-full"
            >
              {tag}
            </span>
          ))}
        </div>
      )}
      <div className="flex flex-col gap-2">
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
  );
};

export default ProjectCard;