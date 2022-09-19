import type { File } from '~/types';

const FilePreview = ({ file }: { file: File }) => {
  if (file.mime.includes('image')) {
    return (
      <img src={file.thumb_url} style={{ width: '100%', maxWidth: 400 }} />
    );
  } else if (file.mime.includes('audio')) {
    return <audio controls src={file.url} />;
  }
  return <video controls src={file.url} />;
};

export default FilePreview;
