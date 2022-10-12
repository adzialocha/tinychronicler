import { useEffect, useState } from 'react';

import request from '~/utils/api';

export default function useChronicle(id?: string | number) {
  const [loading, setLoading] = useState(true);

  const [chronicle, setChronicle] = useState({
    title: '',
    description: '',
    created_at: '',
    language: '',
    id: 0,
  });

  const [files, setFiles] = useState(0);
  const [compositions, setCompositions] = useState(0);

  useEffect(() => {
    const load = async () => {
      if (!id) {
        return;
      }

      setLoading(true);

      const response = await request(['chronicles', id.toString()]);
      setChronicle(response);

      const { total: totalFiles } = await request([
        'chronicles',
        id.toString(),
        'files',
      ]);
      setFiles(totalFiles);

      const { total: totalCompositions } = await request([
        'chronicles',
        id.toString(),
        'compositions',
      ]);
      setCompositions(totalCompositions);

      setLoading(false);
    };

    load();
  }, [id]);

  return { loading, chronicle, files, compositions };
}
