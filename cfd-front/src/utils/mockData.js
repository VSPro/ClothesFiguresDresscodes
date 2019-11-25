/**
 * Подход таков: здесь описываются урлы по которым будут осуществлятся запросы, а также то, что по этим
 * урлам возвращать. В дополнение, тут описывается логика обработки данных, посылаемых в запросе. Этот 
 * файл можно рассматривать, как основу для разработки бэкенда: это и API и примеры обработки данных
 */

import shapeTypeDetermination from './shapeTypeEstimating'

const mockFetch = {}

mockFetch.get = (path, params) => {
    switch (path) {
        case '/find-type-of-shape':
        return shapeTypeDetermination(params.payload)
    }
}

export default mockFetch