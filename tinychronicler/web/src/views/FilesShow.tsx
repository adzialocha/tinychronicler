import { useParams } from 'react-router-dom';
import {
  Anchor,
  Fieldset,
  Hourglass,
  Window,
  WindowContent,
  WindowHeader,
} from 'react95';

import FilePreview from '~/components/FilePreview';
import useFile from '~/hooks/useFile';
import { formatDate } from '~/utils/format';

const FilesShow = () => {
  const { id, chronicleId } = useParams();
  const { file, loading } = useFile(chronicleId, id);

  return loading ? (
    <Hourglass />
  ) : (
    <Window style={{ maxWidth: 800 }}>
      <WindowHeader>{file.name}</WindowHeader>
      <WindowContent>
        <Fieldset label="Preview">
          <FilePreview file={file} />
        </Fieldset>
        <br />
        <Fieldset label="Meta">
          Type: {file.mime}
          <br />
          Uploaded: {formatDate(file.created_at)}
          <br />
          URL: <Anchor href={file.url}>{file.url}</Anchor>
          <br />
        </Fieldset>
      </WindowContent>
    </Window>
  );
};

export default FilesShow;
