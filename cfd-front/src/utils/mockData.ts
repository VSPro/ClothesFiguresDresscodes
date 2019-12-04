/**
 * Подход таков: здесь описываются урлы по которым будут осуществлятся запросы, а также то, что по этим
 * урлам возвращать. В дополнение, тут описывается логика обработки данных, посылаемых в запросе. Этот 
 * файл можно рассматривать, как основу для разработки бэкенда: это и API и примеры обработки данных
 */

import shapeTypeDetermination from './shapeTypeEstimating'
import sizeDetermination from './sizeEstimating'

const mockFetch = { get: {} }

mockFetch.get = (path: any, params: any) => {
    switch (path) {
        case '/find-type-of-shape':
        return {
            shape: shapeTypeDetermination(params.payload),
            sizeParams: {...sizeDetermination(params.payload), shoes: params.payload.shoes}
        }
    }
}

export default mockFetch