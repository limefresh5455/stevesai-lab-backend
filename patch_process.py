import re
with open('src/components/sections/ProcessSection.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    'export default function ProcessSection({ data }: { data?: any }) {',
    '''export default function ProcessSection({ data }: { data?: any }) {
  const activeSteps = data?.steps?.length ? data.steps : steps;
  const titlePrefix = data?.titlePrefix || "How We Build Trust & Deliver";
  const titleHighlight = data?.titleHighlight || "Enterprise AI Excellence";
  const desc = data?.description || "Enterprise AI Solutions. Transform complex data into scalable, high-performance intelligent systems with a transparent, end-to-end engineering lifecycle.";'''
)

content = content.replace('How We Build Trust & Deliver', '{titlePrefix}')
content = content.replace('Enterprise AI Excellence', '{titleHighlight}')
content = content.replace('Enterprise AI Solutions. Transform complex data into scalable,\n              high-performance intelligent systems with a transparent,\n              end-to-end engineering lifecycle.', '{desc}')
content = content.replace('steps.map', 'activeSteps.map')

with open('src/components/sections/ProcessSection.tsx', 'w') as f:
    f.write(content)
