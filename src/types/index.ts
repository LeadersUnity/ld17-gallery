export interface Project {
  id: string;
  studentName: string;
  projectTitle: string;
  description: string;
  unityroomUrl?: string;
  githubReleaseUrl?: string;
  githubUrl: string;
  thumbnail?: string;
  tags?: string[];
}