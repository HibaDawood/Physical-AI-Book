// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Physical AI',
      items: ['physical-ai/chapter1', 'physical-ai/chapter2'],
    },
    {
      type: 'category',
      label: 'Robotics AI',
      items: ['robotics-ai/chapter1', 'robotics-ai/chapter2'],
    },
    {
      type: 'category',
      label: 'Agentic AI',
      items: ['agentic-ai/chapter1', 'agentic-ai/chapter2'],
    },
    {
      type: 'category',
      label: 'Sensors + AI Integration',
      items: ['sensors-ai/chapter1', 'sensors-ai/chapter2'],
    },
    {
      type: 'category',
      label: 'Edge AI',
      items: ['edge-ai/chapter1', 'edge-ai/chapter2'],
    },
  ],
};

module.exports = sidebars;