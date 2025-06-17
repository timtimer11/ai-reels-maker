'use client';

// pages/test-spinner.tsx

import { useState } from 'react';
import { Spinner } from '@/components/ui/loadingSpinner';

export default function TestSpinner() {
  const [show, setShow] = useState(true);
  const [size, setSize] = useState<'small' | 'medium' | 'large'>('medium');

  return (
    <div className="flex flex-col items-center justify-center min-h-screen">
      <h1 className="text-2xl font-bold mb-4">Test Spinner</h1>
      <Spinner size={size} show={show} />
      <div className="mt-4">
        <button onClick={() => setShow(!show)} className="mr-2 px-4 py-2 bg-blue-500 text-white rounded">
          Toggle Spinner
        </button>
        <button onClick={() => setSize('small')} className="mr-2 px-4 py-2 bg-gray-500 text-white rounded">
          Small
        </button>
        <button onClick={() => setSize('medium')} className="mr-2 px-4 py-2 bg-gray-500 text-white rounded">
          Medium
        </button>
        <button onClick={() => setSize('large')} className="px-4 py-2 bg-gray-500 text-white rounded">
          Large
        </button>
      </div>
    </div>
  );
}