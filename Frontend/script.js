// ============ WEB Elements ===========\\
// Templates
const songTemplate = `
    <img src="" class="song-img">
    <div class="song-data">
        <div class="song-info">
            <span class="song-name"></span>
            <span class="song-artist"></span>
        </div>
        <span class="song-priority"></span>
    </div>
    <div class="song-btns">
        <button class="song-delete_btn">Удалить</button>
    </div>`;
const findedSongTemplate = `
    <img class="song-img" id="img" src="">
    <div class="song-info">
        <span class="song-name" id="song"></span>
        <span class="song-artist" id="artist"></span>
    </div>
    <button class="finded-song_btn btn" id="add-song_btn">+</button>`

// Empty States
const nonePlaylist = document.querySelector('.none-playlist')
const nonePlaying = document.querySelector('.not-playing')

// Header
const searchInp = document.getElementById('search-line')
const searchBtn = document.querySelector('.search-btn')

// Playlist Header
const playlist_len = document.getElementById('playlist-len')
const playlist_dur = document.getElementById('playlist-dur')

// Playlist Inner
const playlistUl = document.querySelector('.playlist-songs')
let playlistUl_len = playlistUl.children.length

const playlistPlay = document.getElementById('playlist-play')
const importBtn = document.getElementById('importBtn')

// Player
const player = document.querySelector('.player-container')
const curSong = document.querySelector('.cur_song')
const curSongNav = document.querySelector('.cur_song-nav')

// Import Window
const modal = document.getElementById('import-modal')
const importInput = document.getElementById('import-input')
const modalConfirm = document.getElementById('modal-confirm')
const modalCancel = document.getElementById('modal-cancel')

// Search Results Window
const searchRes = document.getElementById('search-res')
const promptSpan = document.getElementById('prompt-span')
const headerBlur = document.getElementById('header-blur')
const resUl = document.getElementById('resultsUl')
const lenFindedSpan = document.getElementById('len-finded')
const resPH = document.getElementById('res_placeholder')

//=========== Data ===========\\
let playlist = []
let nowPLaying
let isPaused = true

//=========== API ===========\\
const apiAdress = CONFIG.API_URL;

async function apiReq(endpoint, options = {}) {
    const url = apiAdress + endpoint;

    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        }
    };

    try {
        const response = await fetch(url, {
            ...defaultOptions,
            ...options,             
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        });

        if (!response.ok) {
            throw new Error(`Ошибка ${response.status}: ${response.statusText}`);
        }

        const data = await response.json();
        return data;

    } catch (error) {
        console.error('API req error:', error);
        alert('Ошибка соединения с сервером');
        return null;   
    }
}


//=========== Funcsions ===========\\
function UpdatePlaylistInner(plUl) {
    if (plUl.children.length !== 0){
        nonePlaylist.style.display = 'none'
        playlist_len.innerHTML = plUl.children.length
    } else {
        nonePlaylist.style.display = 'flex'
        playlist_len.innerHTML = 0
        playlist_dur.innerText = '0 с'
    }
}

function CreateSongInPlaylist(song, artist, priority, id) {
    const songElement = document.createElement('li')
    songElement.classList.add('song')
    songElement.innerHTML = songTemplate;
    songElement.setAttribute('song-id', id)

    const deleteBtn = songElement.querySelector('.song-delete_btn');
    const prioritySpan = songElement.querySelector('.song-priority');
    const songImg = songElement.querySelector('.song-img');
    const songName = songElement.querySelector('.song-name');
    const songArtist = songElement.querySelector('.song-artist');

    songArtist.innerText = artist
    songName.innerText = song
    prioritySpan.innerText = priority
    prioritySpan.setAttribute('data-priority', priority);
    deleteBtn.setAttribute('song-id', id)

    deleteBtn.addEventListener('click', ()=>{
        songElement.remove()
        UpdatePlaylistInner(playlistUl)
    })

    playlistUl.appendChild(songElement)
    UpdatePlaylistInner(playlistUl)
}
// Search
function showSearchResults(res) {
    resUl.innerHTML = ''

    res.forEach(s => {
        const song = document.createElement('li')
        song.classList.add('finded-song')
        song.innerHTML = findedSongTemplate

        song.querySelector('#img').src = s.img
        song.querySelector('#song').innerText = s.name
        artist = s.artists
        if (artist.length === 1) {
            song.querySelector('#artist').innerText = s.artists[0]

        } else {
            song.querySelector('#artist').innerText = s.artists.join(', ')

        }
        
        resUl.appendChild(song)
    });
}

//============ Event Listeners ===========\\
// Playlist
playlistPlay.addEventListener('click', ()=>{
    if (isPaused){
        if (nowPLaying){
            playlistPlay.innerText = '⏸'

            curSongNav.style.display = 'flex'
            curSong.style.display = 'flex'
            nonePlaying.style.display = 'none'

            isPaused = false
        } else {
            // fetch ask to select song
        }
    } else {
        playlistPlay.innerText = '▶'

        curSongNav.style.display = 'none'
        curSong.style.display = 'none'
        nonePlaying.style.display = 'block'

        isPaused = true
    }
})

// Import Window
importBtn.addEventListener('click', () => {
    modal.style.display = 'flex'  
    importInput.value = ''       
})
modalCancel.addEventListener('click', () => {
    modal.style.display = 'none'
})
modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.style.display = 'none'
    }
})
modalConfirm.addEventListener('click', () => {
    const query = importInput.value.trim()
    if (query) {
        if (query.includes('vk.com/music/playlist')){
            // fetch ask to vk parser
        } else if (query.includes('music.yandex.ru/playlists')){
            // fetch ask to yandex parser
        } else {
            alert('Ссылка не валидна')
        }
    } else {
        alert('Введите ссылку')
    }
})

// Search Results Window
searchBtn.addEventListener('click', async () => {
    let searchPrompt = searchInp.value.trim();
    if (searchPrompt.length === 0) return;

    searchRes.style.display = 'flex';
    headerBlur.style.display = 'flex';
    promptSpan.innerText = searchPrompt;
    resPH.style.display = 'block';
    resPH.innerText = 'Поиск...';
    resUl.innerHTML = '';

    const data = await apiReq(`/search?q=${encodeURIComponent(searchPrompt)}`);

    if (data && data.ok && data.results) {
        resPH.style.display = 'none';
        showSearchResults(data.results);
        lenFindedSpan.innerText = `(${data.results.length})`;
    } else {
        resPH.innerText = 'Ничего не найдено или ошибка сервера';
        lenFindedSpan.innerText = '(0)';
    }
});
searchRes.addEventListener('click', (e)=>{
    if (e.target == searchRes){
        searchRes.style.display = 'none'
        headerBlur.style.display = 'none'

        searchInp.value = ''
        promptSpan.innerText = ''
        lenFindedSpan.innerText = ''
    }
})



if (isPaused){
    playlistPlay.innerText = '▶'
    curSongNav.style.display = 'none'
    curSong.style.display = 'none'
}

nowPLaying = true

CreateSongInPlaylist('song', 'artist', 1, 12)