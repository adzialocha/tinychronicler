import type { File } from '~/types';

const FileThumbnail = ({ file }: { file: File }) => {
  return <img src={file.thumb_url} style={{ width: '100%', maxWidth: 400 }} />;
};

const FilePlayer = ({ file }: { file: File }) => {
  if (file.mime.includes('image')) {
    return null;
  } else if (file.mime.includes('audio')) {
    return <audio controls src={file.url} style={{ width: '100%' }} />;
  }
  return <video controls src={file.url} style={{ width: '100%' }} />;
};

const FilePreview = ({ file }: { file: File }) => {
  return (
    <>
      <FileThumbnail file={file} />
      <br />
      <FilePlayer file={file} />
    </>
  );
};

export default FilePreview;
