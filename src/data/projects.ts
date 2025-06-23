import { Project } from '../types';

export const projects: Project[] = [
  {
    id: '1',
    studentName: 'サンプル研修生1',
    projectTitle: '2Dプラットフォーマー',
    description: 'ジャンプアクションを楽しめる2Dゲームです。様々なステージをクリアしましょう。',
    unityroomUrl: 'https://unityroom.com/games/sample1',
    githubUrl: 'https://github.com/sample/2d-platformer',
    tags: ['2D', 'アクション', 'プラットフォーマー']
  },
  {
    id: '2',
    studentName: 'サンプル研修生2',
    projectTitle: '3Dレーシングゲーム',
    description: 'スピード感あふれるレースゲーム。コースを駆け抜けてベストタイムを目指そう。',
    unityroomUrl: 'https://unityroom.com/games/sample2',
    githubUrl: 'https://github.com/sample/3d-racing',
    tags: ['3D', 'レース', 'スポーツ']
  },
  {
    id: '3',
    studentName: 'サンプル研修生3',
    projectTitle: 'パズルアドベンチャー',
    description: '謎解きを中心としたアドベンチャーゲーム。頭を使って進んでいきましょう。',
    githubReleaseUrl: 'https://github.com/sample/puzzle-adventure/releases',
    githubUrl: 'https://github.com/sample/puzzle-adventure',
    tags: ['パズル', 'アドベンチャー', 'ストーリー']
  }
];