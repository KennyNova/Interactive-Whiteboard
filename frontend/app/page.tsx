'use client'

import dynamic from 'next/dynamic';
import { useState } from 'react';
import { ExcalidrawProps } from '@excalidraw/excalidraw/types/types';

// Dynamically import Excalidraw to avoid SSR issues since it relies on the browser environment
const Excalidraw = dynamic(() => import('@excalidraw/excalidraw').then((mod) => mod.Excalidraw), {
  ssr: false,
});

const ExcalidrawPage = () => {
  // Initial state setup for Excalidraw, can be adjusted as needed
  const [excalidrawProps, setExcalidrawProps] = useState<Partial<ExcalidrawProps>>({
    initialData: null,
  });

  return (
    <div style={{ height: '100vh', width: '100vw' }}>
      <Excalidraw {...excalidrawProps} />
    </div>
  );
};

export default ExcalidrawPage;
