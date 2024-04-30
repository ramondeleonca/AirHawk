import { useState, useEffect } from 'react';

const useFetch = (url: string, options: RequestInit) => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      setIsLoading(true);
      try {
        const response = await fetch(url, options);
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const result = await response.json();
        setData(result);
      } catch (error: unknown) {
        setError(true);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();

    // Cleanup function to cancel any pending requests if the component is unmounted
    return () => {
      // Cleanup code here
    };
  }, [url, options]);

  return { data, error, isLoading };
};

export default useFetch;
