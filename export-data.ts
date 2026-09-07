import fs from 'fs';
import { blogPosts } from './src/data/blogs';
import { services } from './src/data/services';
import { CaseStudiesPosts } from './src/data/case-studies';

const data = {
  blogs: blogPosts,
  services: services,
  caseStudies: CaseStudiesPosts
};

fs.writeFileSync('exported_data.json', JSON.stringify(data, null, 2));
console.log("Data exported to exported_data.json");
