const mockFetch = {}
mockFetch.get = (path, params) => {
    switch (path) {
        case '/':
            return {
                data: 'DataDataDataDataDataDataDataData'
            }
    }
}

export default mockFetch