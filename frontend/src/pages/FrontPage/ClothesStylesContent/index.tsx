import React, { Fragment } from 'react';
import { useStyles } from './styles';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';

interface Content {
  title: string;
  description: string;
  btnText: string;
}

interface Props {
  content: Content;
}

const ClohtesStylesContent: React.FC<Props> = ({ content }) => {
  const { title, description, btnText } = content;
  const {} = useStyles();
  return (
    <Fragment>
      <Typography variant="h5" color="inherit">
        {title}
      </Typography>
      <Typography variant="h6" color="inherit" paragraph>
        {description}
      </Typography>
      <Button>{btnText}</Button>
    </Fragment>
  );
};

export default ClohtesStylesContent;
