import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import Grid from '@material-ui/core/Grid';
import Container from '@material-ui/core/Container';
import Typography from '@material-ui/core/Typography';
import GitHubIcon from '@material-ui/icons/GitHub';
import FacebookIcon from '@material-ui/icons/Facebook';
import TwitterIcon from '@material-ui/icons/Twitter';
import Header from './Header';
import MainFeaturedPost from './MainFeaturedPost';
import FeaturedPost from './FeaturedPost';
import Main from './Main';
import Sidebar from './Sidebar';
import Footer from './Footer';

const useStyles = makeStyles(theme => ({
  mainGrid: {
    marginTop: theme.spacing(3),
  },
  toolbarTitle: {
    flex: 1,
    padding: theme.spacing(0, 0, 4)
  },
}));

const sections = [
  { title: 'О сервисе', url: '#' },
  { title: 'Таблицы размеров', url: '#' },
  { title: 'Об осанке и ногах', url: '#' },
  { title: 'Снятие мерок', url: '#' }
];

const mainFeaturedPost = {
  title: 'Поможем подобрать одежду подстать Вашей фигуре',
  description:
    'Не вся выбераемая одежда сочетается с особенностями внешности человека и с посещаемым человеком местом. Данный сервис предназначен это учесть',
  image: 'https://source.unsplash.com/random',
  imgText: 'main image description',
  linkText: 'Узнать о сервисе больше',
};

const featuredPosts = [
  {
    title: 'Типы фиргур',
    date: '',
    description:
      'Какие бывают, как определяются типы фигур человека и почему это важно',
    image: 'https://source.unsplash.com/random',
    imageText: 'Image Text',
  },
  {
    title: 'Виды дресс-кода',
    date: '',
    description:
      'Какие наряды наиболее уместны в тех или иных случаях и обстановках',
    image: 'https://source.unsplash.com/random',
    imageText: 'Image Text',
  },
  {
    title: 'Особенности внешности',
    date: '',
    description:
      'Цвета волос и кожи, наличие или отсутствие сутулости и прочее - важные черты при правильном подборе одежды',
    image: 'https://source.unsplash.com/random',
    imageText: 'Image Text',
  },
];

const sidebar = {
  title: 'На заметку',
  description:
    'Блок ввода данных определит не только тип фигуры, но и подходящие Вам рамеры одежды, в соответствии с нашими таблицами размеров. Ниже же приведены короткие заметки, связанные с тем, как правельнее снимать мерки, а также ссылки на статьи о принципах работы сервиса',
    links: [
    { title: 'Как снимать мерки', url: '#' },
    { title: 'Типы фигур', url: '#' },
    { title: 'Дресс-коды', url: '#' },
    { title: 'Наши таблицы размеров', url: '#' },
    { title: 'Об осанке и ногах', url: '#' },
  ],
  social: [
    { name: 'GitHub', icon: GitHubIcon },
    { name: 'Twitter', icon: TwitterIcon },
    { name: 'Facebook', icon: FacebookIcon },
  ],
};

export default function Blog() {
  const classes = useStyles();

  return (
    <React.Fragment>
      <CssBaseline />
      <Container maxWidth="lg">
        <Header title="наСтиле. Одежда для подчёркивания достоинств и сглаживания недостаков" sections={sections} />
        <main>
          <MainFeaturedPost post={mainFeaturedPost} />
          <Typography
            component="h2"
            variant="h5"
            color="inherit"
            align="center"
            noWrap
            className={classes.toolbarTitle}
            >
            Три основных принципа при подборе одежды:
          </Typography>
          <Grid container spacing={4}>
            {featuredPosts.map(post => (
              <FeaturedPost key={post.title} post={post} />
            ))}
          </Grid>
          <Grid container spacing={5} className={classes.mainGrid}>
            <Main 
                title1="Определить тип фигуры и подходящие размеры одежды:"
                title2="Задать дополнитиельные размеры и указать особенности внешнего вида:"    
            />
            <Sidebar
              title={sidebar.title}
              description={sidebar.description}
              links={sidebar.links}
              social={sidebar.social}
            />
          </Grid>
        </main>
      </Container>
      <Footer title="Footer" description="Something here to give the footer a purpose!" />
    </React.Fragment>
  );
}