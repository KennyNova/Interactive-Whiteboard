import React, { useRef, useEffect } from 'react';
import { Tldraw } from 'tldraw'; 

const Whiteboard: React.FC = () => {
  const whiteboardRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (whiteboardRef.current) {
      const tldraw = new Tldraw({
        container: whiteboardRef.current,
        defaultTool: tldraw.shapes.Rectangle, // Access through the tldraw instance
      });
    }
  }, []);

  return <div ref={whiteboardRef} style={{ width: '100vw', height: '100vh' }} />; 
};

export default Whiteboard;
