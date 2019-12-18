/**
 * Ф-ция обработки данных, введённых полозователем. Если обработка будет на фронте,
 * то эту ф-цию надо вызвать в саге
 * Методика расчёта описана в файле гугл-док, ссылка на который приведена в README
 */
export default function shapeTypeDetermination({
  shoulders,
  waist,
  hips,
  height,
  sex
}: {
  shoulders: number;
  waist: number;
  hips: number;
  height: number;
  sex: string;
}) {
  /**
   * Ф-ция определения удлинения тела
   * @param {number} shoulders
   * @param {number} height
   * @param {string} sex
   */
  function elongationDetermination(
    shoulders: number,
    height: number,
    sex: string
  ) {
    // Потребуется уточнить параметры для кажного из полов
    // Эти данные можно сделать в виде параметра
    const elongationFields_M = [6, 4.5, 3.5]; // [6, 4.5, 3.5, 2.5]
    const elongationFields_F = [6, 4.5, 3.5];

    const elongation = +height / +shoulders;
    // Чем выше категория, тем шире человек
    let categoryByElongation = null;
    if (sex === "m") {
      if (
        elongation > elongationFields_M[0] ||
        elongation < elongationFields_M[elongationFields_M.length]
      ) {
        return 0;
      }
      elongationFields_M.reduce((acc, item, index) => {
        if (acc <= item) {
          categoryByElongation = ++index;
        }
        return acc;
      }, elongation);
    } else {
      if (
        elongation > elongationFields_F[0] ||
        elongation < elongationFields_F[elongationFields_F.length]
      ) {
        return 0;
      }
      elongationFields_F.reduce((acc, item, index) => {
        if (acc <= item) {
          categoryByElongation = ++index;
        }
        return acc;
      }, elongation);
    }
    return categoryByElongation;
  }

  /**
   * Ф-ция определения превалирующего размера, определяемого скилетом
   * @param {number} shoulders
   * @param {number} hips
   */
  function majorSizeDetermination(
    shoulders: number,
    hips: number,
    sex: string
  ) {
    // Потребуется уточнить параметры для кажного из полов
    // Эти данные можно сделать в виде параметра
    const majorSizeFields_M = [0.7, 1, 1.2]; // [0.7, 1, 1.2, 1.5]
    const majorSizeFields_F = [0.7, 1, 1.2];

    const hipsProjection = +hips / 3;
    const ratioOfSizes = hipsProjection / shoulders;

    // Чем выше категория, тем шире бёдра
    let categoryByMajorSize = null;
    if (sex === "m") {
      if (
        ratioOfSizes < majorSizeFields_M[0] ||
        ratioOfSizes > majorSizeFields_M[majorSizeFields_M.length]
      ) {
        return 0;
      }
      majorSizeFields_M.reduce((acc: any, item: any, index: number) => {
        if (acc >= item) {
          categoryByMajorSize = ++index;
        }
        return acc;
      }, ratioOfSizes);
    } else {
      if (
        ratioOfSizes < majorSizeFields_F[0] ||
        ratioOfSizes > majorSizeFields_F[majorSizeFields_F.length]
      ) {
        return 0;
      }
      majorSizeFields_F.reduce((acc: any, item: any, index: number) => {
        if (acc >= item) {
          categoryByMajorSize = ++index;
        }
        return acc;
      }, ratioOfSizes);
    }
    return categoryByMajorSize;
  }

  /**
   * Определение степени толстоты человека
   * @param {number} shoulders
   * @param {number} waist
   * @param {number} hips
   * @param {string} sex
   */
  function degreeOfWidth(
    shoulders: number,
    waist: number,
    hips: number,
    sex: string
  ) {
    // Потребуется уточнить параметры для кажного из полов
    // Эти данные можно сделать в виде параметра
    const degreeOfWidthFields_M = [1.5, 1.1, 0.8]; // [1.5, 1.1, 0.8, 0.5]
    const degreeOfWidthFields_F = [1.5, 1.1, 0.8];

    const chest = +shoulders * 3;
    const middleWidth = (+hips + chest) / 2;
    const ratioOfSizes = middleWidth / waist;
    let categoryByDegreeOfWidth = null;
    // Чем выше категория, тем толще талия
    if (sex === "m") {
      if (
        ratioOfSizes > degreeOfWidthFields_M[0] ||
        ratioOfSizes < degreeOfWidthFields_M[degreeOfWidthFields_M.length]
      ) {
        return 0;
      }
      degreeOfWidthFields_M.reduce((acc: any, item: any, index: number) => {
        if (acc <= item) {
          categoryByDegreeOfWidth = ++index;
        }
        return acc;
      }, ratioOfSizes);
    } else {
      if (
        ratioOfSizes > degreeOfWidthFields_F[0] ||
        ratioOfSizes < degreeOfWidthFields_F[degreeOfWidthFields_F.length]
      ) {
        return 0;
      }
      degreeOfWidthFields_F.reduce((acc: any, item: any, index: number) => {
        if (acc <= item) {
          categoryByDegreeOfWidth = ++index;
        }
        return acc;
      }, ratioOfSizes);
    }
    return categoryByDegreeOfWidth;
  }

  /**
   * Ф-ция определения типа фигуры человека на основе ключевых показателей
   * @param {number} shoulders
   * @param {number} waist
   * @param {number} hips
   * @param {number} height
   * @param {string} sex
   */
  function estimateTypeOfShape(
    shoulders: number,
    waist: number,
    hips: number,
    height: number,
    sex: string
  ) {
    const categoryByElongation: any = elongationDetermination(
      shoulders,
      height,
      sex
    );
    const categoryByMajorSize: any = majorSizeDetermination(
      shoulders,
      hips,
      sex
    );
    const categoryByDegreeOfWidth: any = degreeOfWidth(
      shoulders,
      waist,
      hips,
      sex
    );

    // TODO: Написано не оптимально, проверку на сообветствие можно сделать раньше
    let typeOfShape = [];
    typeOfShape.push(categoryByElongation);
    if (
      (categoryByMajorSize === 1 || categoryByMajorSize === 2) &&
      (categoryByDegreeOfWidth === 1 || categoryByDegreeOfWidth === 2)
    ) {
      typeOfShape.push("A");
    } else if (
      categoryByMajorSize === 3 &&
      (categoryByDegreeOfWidth === 1 || categoryByDegreeOfWidth === 2)
    ) {
      typeOfShape.push("B");
    } else if (
      (categoryByMajorSize === 1 ||
        categoryByMajorSize === 2 ||
        categoryByMajorSize === 3) &&
      categoryByDegreeOfWidth === 3
    ) {
      typeOfShape.push("C");
    } else {
      console.log(
        categoryByElongation,
        categoryByMajorSize,
        categoryByDegreeOfWidth
      );
      return "data is not correct";
    }
    return typeOfShape;
  }
  return estimateTypeOfShape(shoulders, waist, hips, height, sex);
}
