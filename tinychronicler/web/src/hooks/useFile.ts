import { useEffect, useState } from 'react';

import type { File } from '~/types';

import request from '~/utils/api';

export default function useFile(
  chronicleId?: number | string,
  id?: number | string,
) {
  const [loading, setLoading] = useState(true);

  const [file, setFile] = useState<File>({
    created_at: '',
    id: 0,
    mime: '',
    name: '',
    thumb_name: '',
    thumb_url: '',
    url: '',
  });

  useEffect(() => {
    const load = async () => {
      if (!id || !chronicleId) {
        return;
      }

      setLoading(true);

      const response = await request([
        'chronicles',
        chronicleId.toString(),
        'files',
        id.toString(),
      ]);
      setFile(response);

      setLoading(false);
    };

    load();
  }, [chronicleId, id]);

  return { loading, file };
}
