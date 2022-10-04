import { Fragment, useState, createRef } from 'react';
import { useFormik } from 'formik';
import { useNavigate, useParams, useSearchParams } from 'react-router-dom';
import * as Yup from 'yup';
import {
  Button,
  Hourglass,
  Tab,
  TabBody,
  Fieldset,
  Table,
  TableBody,
  TableDataCell,
  TableHead,
  TableHeadCell,
  TableRow,
  Tabs,
  TextField,
  Window,
  WindowContent,
  WindowHeader,
} from 'react95';

import type { Chronicle, File, Composition } from '~/types';

import Link from '~/components/Link';
import Paginator from '~/components/Paginator';
import request from '~/utils/api';
import useChronicle from '~/hooks/useChronicle';
import { formatDate } from '~/utils/format';

const ALLOWED_FILES = '.wav,.png,.jpg,.mp4,.mpeg';

const EditInfo = ({ chronicle }: { chronicle: Chronicle }) => {
  const navigate = useNavigate();

  const { title, description } = chronicle;

  const formik = useFormik({
    initialValues: { title, description },
    validationSchema: Yup.object({
      title: Yup.string().max(255).required(),
      description: Yup.string().required(),
    }),
    onSubmit: async (values, { setSubmitting }) => {
      try {
        await request(['chronicles', chronicle.id.toString()], values, 'PUT');
        navigate('/chronicles');
      } catch {
        window.alert('Something went wrong');
      }

      setSubmitting(false);
    },
  });

  return (
    <form onSubmit={formik.handleSubmit}>
      <Fieldset label="Meta">
        Created {formatDate(chronicle.created_at)}
      </Fieldset>
      <br />
      <Fieldset label="Fields">
        <fieldset>
          <label htmlFor="title">Title</label>
          <TextField
            id="title"
            name="title"
            value={formik.values.title}
            onChange={formik.handleChange}
            fullWidth
          />
          {formik.touched.title && Boolean(formik.errors.title) && (
            <p>
              <em>{formik.errors.title}</em>
            </p>
          )}
        </fieldset>
        <fieldset>
          <label htmlFor="description">Description</label>
          <TextField
            id="description"
            name="description"
            multiline
            rows={4}
            value={formik.values.description}
            onChange={formik.handleChange}
            fullWidth
          />
          {formik.touched.description && Boolean(formik.errors.description) && (
            <p>
              <em>{formik.errors.description}</em>
            </p>
          )}
        </fieldset>
      </Fieldset>
      <div style={{ paddingTop: 7 }}>
        <Button type="submit">Update</Button>
      </div>
    </form>
  );
};

const EditFiles = ({ chronicle }: { chronicle: Chronicle }) => {
  const [search, setSearch] = useSearchParams();
  const uploader = createRef<HTMLInputElement>();
  const { compositions } = useChronicle(chronicle.id.toString());
  const page = search.get('page');
  const [loading, setLoading] = useState(false);

  const onClick = () => {
    uploader.current?.click();
  };

  const onDelete = async (fileId: number) => {
    const answer = window.confirm('Are you sure?');

    if (answer) {
      setLoading(true);

      try {
        await request(
          ['chronicles', chronicle.id.toString(), 'files', fileId.toString()],
          undefined,
          'DELETE',
        );
      } catch (error) {
        window.alert(error);
      }

      setLoading(false);
    }
  };

  const onUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;

    if (!files || files.length === 0) {
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append('file', files[0]);

    try {
      await request(
        ['chronicles', chronicle.id.toString(), 'files'],
        formData,
        'POST',
      );
    } catch (error) {
      window.alert(error);
    }

    event.target.value = '';

    setLoading(false);
  };

  return (
    <Fragment>
      <input
        style={{ display: 'none' }}
        type="file"
        ref={uploader}
        accept={ALLOWED_FILES}
        onChange={onUpload}
      />
      {loading ? (
        <Hourglass />
      ) : (
        <Paginator<File>
          page={page ? parseInt(page, 10) : 1}
          onChange={(page) => {
            setSearch({ page: page.toString(), tab: 'files' });
          }}
          path={['chronicles', chronicle.id.toString(), 'files']}
        >
          {({
            items,
            hasPreviousPage,
            hasNextPage,
            nextPage,
            previousPage,
          }) => (
            <>
              <Table>
                <TableHead>
                  <TableRow head>
                    <TableHeadCell>ID</TableHeadCell>
                    <TableHeadCell>Name</TableHeadCell>
                    <TableHeadCell>Type</TableHeadCell>
                    <TableHeadCell>Created At</TableHeadCell>
                    <TableHeadCell>Actions</TableHeadCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {items.map((file) => {
                    return (
                      <TableRow key={file.id}>
                        <TableDataCell>{file.id}</TableDataCell>
                        <TableDataCell>{file.name}</TableDataCell>
                        <TableDataCell>
                          {file.mime.includes('image') && '🖼️'}
                          {file.mime.includes('audio') && '🎧'}
                          {file.mime.includes('video') && '🎥'}
                        </TableDataCell>
                        <TableDataCell>
                          {formatDate(file.created_at)}
                        </TableDataCell>
                        <TableDataCell>
                          <Link
                            to={`/chronicles/${chronicle.id}/files/${file.id}`}
                            variant="flat"
                            size="sm"
                          >
                            Show
                          </Link>
                          &nbsp;
                          <Link
                            disabled={compositions > 0}
                            onClick={() => onDelete(file.id)}
                            variant="flat"
                            size="sm"
                          >
                            Delete
                          </Link>
                        </TableDataCell>
                      </TableRow>
                    );
                  })}
                </TableBody>
              </Table>
              <div
                style={{
                  display: 'flex',
                  paddingTop: 7,
                  justifyContent: 'space-between',
                }}
              >
                <div>
                  <Link disabled={!hasPreviousPage} onClick={previousPage}>
                    &lt;
                  </Link>
                  <Link disabled={!hasNextPage} onClick={nextPage}>
                    &gt;
                  </Link>
                </div>
                <Link onClick={onClick}>Upload file</Link>
              </div>
            </>
          )}
        </Paginator>
      )}
    </Fragment>
  );
};

const EditCompositions = ({ chronicle }: { chronicle: Chronicle }) => {
  const { files } = useChronicle(chronicle.id.toString());
  const [search, setSearch] = useSearchParams();
  const page = search.get('page');
  const [loading, setLoading] = useState(false);

  const onGenerate = async () => {
    setLoading(true);

    try {
      await request(
        ['chronicles', chronicle.id.toString(), 'compositions'],
        undefined,
        'POST',
      );
    } catch (error) {
      window.alert(error);
    }

    setLoading(false);
  };

  const onDelete = async (compositionId: number) => {
    const answer = window.confirm('Are you sure?');

    if (answer) {
      setLoading(true);

      try {
        await request(
          [
            'chronicles',
            chronicle.id.toString(),
            'compositions',
            compositionId.toString(),
          ],
          undefined,
          'DELETE',
        );
      } catch (error) {
        window.alert(error);
      }

      setLoading(false);
    }
  };

  return files > 0 ? (
    <Paginator<Composition>
      page={page ? parseInt(page, 10) : 1}
      onChange={(page) => {
        setSearch({ page: page.toString(), tab: 'compositions' });
      }}
      path={['chronicles', chronicle.id.toString(), 'compositions']}
    >
      {({ items, hasPreviousPage, hasNextPage, nextPage, previousPage }) => (
        <>
          <Table>
            <TableHead>
              <TableRow head>
                <TableHeadCell>ID</TableHeadCell>
                <TableHeadCell>Title</TableHeadCell>
                <TableHeadCell>Created At</TableHeadCell>
                <TableHeadCell>Actions</TableHeadCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {items.map((composition) => {
                return (
                  <TableRow key={composition.id}>
                    <TableDataCell>{composition.id}</TableDataCell>
                    <TableDataCell>{composition.title}</TableDataCell>
                    <TableDataCell>
                      {formatDate(composition.created_at)}
                    </TableDataCell>
                    <TableDataCell>
                      <Link
                        to={`/chronicles/${chronicle.id}/compositions/${composition.id}`}
                        variant="flat"
                        size="sm"
                      >
                        Show
                      </Link>
                      &nbsp;
                      <Link
                        onClick={() => onDelete(composition.id)}
                        variant="flat"
                        size="sm"
                      >
                        Delete
                      </Link>
                    </TableDataCell>
                  </TableRow>
                );
              })}
            </TableBody>
          </Table>
          <div
            style={{
              display: 'flex',
              paddingTop: 7,
              justifyContent: 'space-between',
            }}
          >
            <div>
              <Link disabled={!hasPreviousPage} onClick={previousPage}>
                &lt;
              </Link>
              <Link disabled={!hasNextPage} onClick={nextPage}>
                &gt;
              </Link>
            </div>
            <Link disabled={loading} onClick={onGenerate}>
              Generate composition
            </Link>
          </div>
        </>
      )}
    </Paginator>
  ) : (
    <p>Upload at least one audio file before generating a composition.</p>
  );
};

const ChroniclesEdit = () => {
  const { id } = useParams();
  const [search, setSearch] = useSearchParams();
  const activeTab = search.get('tab') ? search.get('tab') : 'info';
  const { chronicle, loading } = useChronicle(id);

  const handleChange = (
    _event: React.MouseEvent<HTMLElement>,
    value: string,
  ) => {
    setSearch({ tab: value });
  };

  return loading ? (
    <Hourglass />
  ) : (
    <Window style={{ width: '100%', maxWidth: 800 }}>
      <WindowHeader>Edit "{chronicle.title}" Chronicle</WindowHeader>
      <WindowContent>
        <Tabs value={activeTab} onChange={handleChange}>
          <Tab value="info">Chronicle</Tab>
          <Tab value="files">Files</Tab>
          <Tab value="compositions">Compositions</Tab>
        </Tabs>
        <TabBody>
          {activeTab === 'info' && <EditInfo chronicle={chronicle} />}
          {activeTab === 'files' && <EditFiles chronicle={chronicle} />}
          {activeTab === 'compositions' && (
            <EditCompositions chronicle={chronicle} />
          )}
        </TabBody>
      </WindowContent>
    </Window>
  );
};

export default ChroniclesEdit;
