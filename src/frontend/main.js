import './style.css'
import {handleInteractionChange, initInteractionStates, pollBackendInteractionStates} from "./interactions.js"
import {inputIsValid, sendMessage} from "./chat.js"
import {displayProducts} from "./products.js";

const firebaseConfig = {
    apiKey: "AIzaSyDjHYcpkOwp_fLoxlxSK-IJ8s9hMJjCXuM", // pragma: allowlist secret
    authDomain: "chat-app-front-end.firebaseapp.com",
    projectId: "chat-app-front-end",
    storageBucket: "chat-app-front-end.appspot.com",
    messagingSenderId: "648539574693",
    appId: "1:648539574693:web:6ff5288ead51072ea9584c",
    measurementId: "G-9SNCM0SG3F"
};

let sessionChatHistory = [];
let sessionId;

// API endpoints
const chatBotUrl = 'http://localhost:5000/api/send_message';
const healthCheckUrl = 'http://localhost:5000/api/health';
const setStateUrl = 'http://localhost:5000/api/set_input_state';
const getStateUrl = 'http://localhost:5000/api/get_input_state';
const initSession = 'http://localhost:5000/api/init_session';


// UI
document.querySelector('#app').innerHTML = `
    <div id="outer-content-container" >
        <div id="outer-chat-container" class="main-container">
            <h1 id="header-text" class="unselectable">🧑 💬 🤖</h1>
            <div id="chat-history-container" class="main-container">
            </div>
            <div id="input-container">
                <input id="text-input" type="text" value="" placeholder="Say something..." required>
                <input id="submit-button" type="submit" value="submit">
            </div>

        </div>
        <div id="interactions-outer">
                <h2 id="header-text" class="unselectable">Form Controls:</h2>
            <div id="interactions-container" class="main-container">

                <div id="filter-container">
                    <div id="api-label">Search: </div>
                    <input id="filter" type="text" name="wildlife" value="">
                </div>
                <hr class="solid">

            </div>
        </div>
        <div id="products-outer">
            <h2 id="header-text" class="unselectable">Products:</h2>
            <div id="products-container" class="main-container"></div>
        </div>
    </div>
`


// Product display

const products = '{' +
    '"id":{"0":385687,"1":502356,"2":569094,"3":536437,"4":667538,"5":890771,"6":447277,"7":713704,"8":447365,"9":840326,"10":758323,"11":799379,"12":605886,"13":882569,"14":552688,"15":893712,"16":842675,"17":1105803,"18":934433,"19":931102},' +
    '"backdrop_path":{"0":"\\/2e7fc8eNwLXZ5Uvehvl3xj8wVyv.jpg","1":"\\/9n2tJBplPbgR2ca05hS5CKXwP2c.jpg","2":"\\/nGxUxi3PfXDRm7Vg95VBNgNM8yc.jpg","3":"\\/8FhKnPpql374qyyHAkZDld93IUw.jpg","4":"\\/9NgtktUFLm9cnFDFaekx2ROh84f.jpg","5":"\\/9t0tJXcOdWwwxmGTk112HGDaT0Q.jpg","6":"\\/ribiMu3iINPxDkofErPxe8jQ8L0.jpg","7":"\\/aAgGrfBwna1nO4M2USxwFgK5O0t.jpg","8":"\\/5YZbUmjbMa3ClvSW1Wj3D6XGolb.jpg","9":"\\/94TIUEhuwv8PhdIADEvSuwPljS5.jpg","10":"\\/hiHGRbyTcbZoLsYYkO4QiCLYe34.jpg","11":"\\/xkXsV1WOiKfAJ6dzXiavdwsZ3E2.jpg","12":"\\/T5xXoFqyc9jNXZIbH4Sw0jwWjw.jpg","13":"\\/eTvN54pd83TrSEOz6wbsXEJktCV.jpg","14":"\\/i1eghEBiC0gN4KnwuUGC2fNiX1f.jpg","15":"\\/jAmmb9RApuRckDJtYWeOgBUgQyG.jpg","16":"\\/qElNES0sHVQcbzvGrTx7ccpGzij.jpg","17":"\\/rOKBBs0Hn4yu60wDF7xZUH7CVgh.jpg","18":"\\/44immBwzhDVyjn87b3x3l9mlhAD.jpg","19":"\\/uH1cuq2hmZn5B4oiR9a1l4Wy91I.jpg"},' +
    '"genre_ids":{"0":["Action","Crime","Thriller"],"1":["Adventure","Animation","Comedy","Family","Fantasy"],"2":["Action","Adventure","Animation","Science Fiction"],"3":["Mystery","Science Fiction","Thriller"],"4":["Action","Adventure","Science Fiction"],"5":["Horror","Thriller"],"6":["Adventure","Family","Fantasy","Romance"],"7":["Horror","Thriller"],"8":["Action","Adventure","Science Fiction"],"9":["Action","War"],"10":["Horror","Thriller"],"11":["Action","Horror","Thriller"],"12":["Action","Crime","Mystery","Thriller"],"13":["Action","Thriller","War"],"14":["Action","Thriller"],"15":["Action","Animation","Fantasy","Science Fiction"],"16":["Action","Drama","Science Fiction"],"17":["Action","Crime","Thriller"],"18":["Horror","Mystery","Thriller"],"19":["Action","Adventure","Comedy","Drama"]},' +
    '"original_language":{"0":"en","1":"en","2":"en","3":"en","4":"en","5":"en","6":"en","7":"en","8":"en","9":"fi","10":"en","11":"ko","12":"en","13":"en","14":"en","15":"ja","16":"zh","17":"en","18":"en","19":"zh"},' +
    '"original_title":{"0":"Fast X","1":"The Super Mario Bros. Movie","2":"Spider-Man: Across the Spider-Verse","3":"Hypnotic","4":"Transformers: Rise of the Beasts","5":"The Black Demon","6":"The Little Mermaid","7":"Evil Dead Rise","8":"Guardians of the Galaxy Vol. 3","9":"Sisu","10":"The Pope\'s Exorcist","11":"\\ub291\\ub300\\uc0ac\\ub0e5","12":"To Catch a Killer","13":"Guy Ritchie\'s The Covenant","14":"The Mother","15":"\\u5287\\u5834\\u7248 \\u30bd\\u30fc\\u30c9\\u30a2\\u30fc\\u30c8\\u30fb\\u30aa\\u30f3\\u30e9\\u30a4\\u30f3 -\\u30d7\\u30ed\\u30b0\\u30ec\\u30c3\\u30b7\\u30d6- \\u51a5\\u304d\\u5915\\u95c7\\u306e\\u30b9\\u30b1\\u30eb\\u30c4\\u30a9","16":"\\u6d41\\u6d6a\\u5730\\u74032","17":"Snag","18":"Scream VI","19":"Long ma jing shen"},' +
    '"overview":{"0":"Over many missions and against impossible odds, Dom Toretto and his family have outsmarted, out-nerved and outdriven every foe in their path. Now, they confront the most lethal opponent they\'ve ever faced: A terrifying threat emerging from the shadows of the past who\'s fueled by blood revenge, and who is determined to shatter this family and destroy everything\\u2014and everyone\\u2014that Dom loves, forever.","1":"While working underground to fix a water main, Brooklyn plumbers\\u2014and brothers\\u2014Mario and Luigi are transported down a mysterious pipe and wander into a magical new world. But when the brothers are separated, Mario embarks on an epic quest to find Luigi.","2":"After reuniting with Gwen Stacy, Brooklyn\\u2019s full-time, friendly neighborhood Spider-Man is catapulted across the Multiverse, where he encounters the Spider Society, a team of Spider-People charged with protecting the Multiverse\\u2019s very existence. But when the heroes clash on how to handle a new threat, Miles finds himself pitted against the other Spiders and must set out on his own to save those he loves most.","3":"A detective becomes entangled in a mystery involving his missing daughter and a secret government program while investigating a string of reality-bending crimes.","4":"When a new threat capable of destroying the entire planet emerges, Optimus Prime and the Autobots must team up with a powerful faction known as the Maximals. With the fate of humanity hanging in the balance, humans Noah and Elena will do whatever it takes to help the Transformers as they engage in the ultimate battle to save Earth.","5":"Oilman Paul Sturges\' idyllic family vacation turns into a nightmare when they encounter a ferocious megalodon shark that will stop at nothing to protect its territory. Stranded and under constant attack, Paul and his family must somehow find a way to get his family back to shore alive before it strikes again in this epic battle between humans and nature.","6":"The youngest of King Triton\\u2019s daughters, and the most defiant, Ariel longs to find out more about the world beyond the sea, and while visiting the surface, falls for the dashing Prince Eric. With mermaids forbidden to interact with humans, Ariel makes a deal with the evil sea witch, Ursula, which gives her a chance to experience life on land, but ultimately places her life \\u2013 and her father\\u2019s crown \\u2013 in jeopardy.","7":"Three siblings find an ancient vinyl that gives birth to bloodthirsty demons that run amok in a Los Angeles apartment building and thrusts them into a primal battle for survival as they face the most nightmarish version of family imaginable.\\"","8":"Peter Quill, still reeling from the loss of Gamora, must rally his team around him to defend the universe along with protecting one of their own. A mission that, if not completed successfully, could quite possibly lead to the end of the Guardians as we know them.","9":"Deep in the wilderness of Lapland, Aatami Korpi is searching for gold but after he stumbles upon Nazi patrol, a breathtaking and gold-hungry chase through the destroyed and mined Lapland wilderness begins.","10":"Father Gabriele Amorth, Chief Exorcist of the Vatican, investigates a young boy\'s terrifying possession and ends up uncovering a centuries-old conspiracy the Vatican has desperately tried to keep hidden.","11":"While under heavily armed guard, the dangerous convicts aboard a cargo ship unite in a coordinated escape attempt that soon escalates into a bloody, all-out riot. But as the fugitives continue their brutal campaign of terror, they soon discover that not even the most vicious among them is safe from the horror they unknowingly unleashed from the darkness below deck.","12":"Baltimore. New Year\'s Eve. A talented but troubled police officer is recruited by the FBI\'s chief investigator to help profile and track down a mass murderer.","13":"During the war in Afghanistan, a local interpreter risks his own life to carry an injured sergeant across miles of grueling terrain.","14":"A deadly female assassin comes out of hiding to protect the daughter that she gave up years before, while on the run from dangerous men.","15":"Over a month has passed since 10,000 users were trapped inside the \\"Sword Art Online\\" world. Asuna, who cleared the first floor of the floating iron castle of Aincrad, joined up with Kirito and continued her journey to reach the top floor. With the support of female Information Broker Argo, clearing the floors seemed to be progressing smoothly, but conflict erupts between two major guilds who should be working together \\u2013 the top player groups ALS (the Aincrad Liberation Squad) and DKB (the Dragon Knights Brigade). And meanwhile, behind the scenes exists a mysterious figure pulling the strings\\u2026","16":"A prequel to The Wandering Earth.","17":"An Australian lone wolf\'s quiet existence is shattered when he learns that the woman he once loved and thought was dead is alive and held captive by ruthless gangsters. Now, to take on this dangerous criminal organization, he must seek out allies and storm into a world of violence to rescue the love of his life in this gritty, modern day violent fairytale.","18":"Following the latest Ghostface killings, the four survivors leave Woodsboro behind and start a fresh chapter.","19":"The once beautiful, now down-and-out Dragon Tiger martial artist Lao Luo lives with his beloved horse, Red Rabbit. Due to a debt dispute involving Red Rabbit, he is faced with the crisis of \\"father-son separation\\". In desperation, Lao Luo asks his daughter Bao and her boyfriend Naihua, who have misunderstood him for years, for help. On the road of self-help of three people and one horse, they make a lot of jokes and gradually get closer to each other."},"poster_path":{"0":"\\/fiVW06jE7z9YnO4trhaMEdclSiC.jpg","1":"\\/qNBAXBIQlnOThrVvA6mA2B5ggV6.jpg","2":"\\/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg","3":"\\/3IhGkkalwXguTlceGSl8XUJZOVI.jpg","4":"\\/gPbM0MK8CP8A174rmUwGsADNYKD.jpg","5":"\\/uiFcFIjig0YwyNmhoxkxtAAVIL2.jpg","6":"\\/ym1dxyOk4jFcSl4Q2zmRrA5BEEN.jpg","7":"\\/5ik4ATKmNtmJU6AYD0bLm56BCVM.jpg","8":"\\/r2J02Z2OpNTctfOSN1Ydgii51I3.jpg","9":"\\/ygO9lowFMXWymATCrhoQXd6gCEh.jpg","10":"\\/gNPqcv1tAifbN7PRNgqpzY8sEJZ.jpg","11":"\\/dniWicB6fa7NvpGbguxWlNPMc5f.jpg","12":"\\/mFp3l4lZg1NSEsyxKrdi0rNK8r1.jpg","13":"\\/jZy73aPYrwwhuc37ALgnJUCaTnK.jpg","14":"\\/vnRthEZz16Q9VWcP5homkHxyHoy.jpg","15":"\\/2lEyzOq6ILNgBpLLpTRckQhbNNt.jpg","16":"\\/pR858ihc6Ls9xohpdRJVjV787ml.jpg","17":"\\/nhj4Q39qMSk6X5Ly9j9Yqyjrg5A.jpg","18":"\\/wDWwtvkRRlgTiUr6TyLSMX8FCuZ.jpg","19":"\\/ukFo9pwVJ5mzTgmFCanYsYC4roF.jpg"},' +
    '"release_date":{"0":"2023-05-17","1":"2023-04-05","2":"2023-05-31","3":"2023-05-11","4":"2023-06-06","5":"2023-04-26","6":"2023-05-18","7":"2023-04-12","8":"2023-05-03","9":"2023-01-27","10":"2023-04-05","11":"2022-09-21","12":"2023-04-06","13":"2023-04-19","14":"2023-05-04","15":"2022-10-22","16":"2023-01-22","17":"2023-04-28","18":"2023-03-08","19":"2023-04-07"},' +
    '"title":{"0":"Fast X","1":"The Super Mario Bros. Movie","2":"Spider-Man: Across the Spider-Verse","3":"Hypnotic","4":"Transformers: Rise of the Beasts","5":"The Black Demon","6":"The Little Mermaid","7":"Evil Dead Rise","8":"Guardians of the Galaxy Vol. 3","9":"Sisu","10":"The Pope\'s Exorcist","11":"Project Wolf Hunting","12":"To Catch a Killer","13":"Guy Ritchie\'s The Covenant","14":"The Mother","15":"Sword Art Online the Movie -Progressive- Scherzo of Deep Night","16":"The Wandering Earth II","17":"Snag","18":"Scream VI","19":"Ride On"}' +
    '}';
const products_json = JSON.parse(products);
const genres = ["Adventure", "Action", "Fantasy", "Mystery", "Comedy", "Romance", "Family", "Crime", "Drama", "Horror", "War", "Science Fiction", "Thriller", "Animation"].sort();

// UI Element functions
function getChatElements() {
    return {
        "submitButton": document.querySelector('#submit-button'),
        "textBox": document.querySelector('#text-input')
    }
}

function getInteractionElements() {
    const interactionContainer = document.querySelector('#interactions-container');
    return interactionContainer.querySelectorAll('input');
}


function createGenreElements(genres) {
    const interactionContainer = document.querySelector('#interactions-container');
    const genreContainer = document.createElement('div');
    genreContainer.id = "genre-container";
    interactionContainer.append(genreContainer);
    genres.forEach((genre) => {
        const genreBox = document.createElement('div');
        const genreElement = document.createElement('input');
        genreElement.type = 'checkbox';
        genreElement.id = genre;
        genreElement.name = genre;
        genreElement.value = genre;
        genreBox.append(genreElement);
        const genreLabel = document.createElement('label');
        genreLabel.htmlFor = genre;
        genreLabel.innerHTML = genre;
        genreBox.append(genreLabel);
        genreContainer.append(genreBox);
    });
}


// UI State functions
async function initilizeBackendConnection(url = healthCheckUrl, currentState) {
    try {
        const headers = {"Content-Type": "application/json"}
        const requestInit = {
            method: "post",
            mode: "cors",
            headers: headers,
            body: JSON.stringify(currentState),
            credentials: "include"
        }
        const response = await fetch(
            url,
            requestInit
        );
        if (response.ok) {
            document.querySelector('#header-text').innerHTML = '🧑 💬 🤖';
            return response.json();
        }
    } catch (e) {
        console.log(e.message);
    }
    console.log('not healthy, is the backend running?');
    document.querySelector('#header-text').innerHTML = '🧑 💬 🚫🤖🚫(offline)';
    document.querySelector('#text-input').disabled = true;
    document.querySelector('#submit-button').disabled = true;
    return null;
}

function chatboxListeners(url, database, elements, validator, localMemory, sessionId) {
    // listeners to handle user submitting messages (either push enter or click submit)
    const message = {
        url: url,
        database: database,
        textElement: elements['textBox'],
        validator: validator,
        localMemory: localMemory,
        sessionId: sessionId
    }
    elements['submitButton'].addEventListener('click', () => sendMessage(message));
    elements['textBox'].addEventListener('keydown', (event) => {
        event.key === 'Enter' ? sendMessage(message) : null;
    });
}

function interactionListeners(interactionState, interactionElements) {
    interactionElements.forEach((interactionElement) => {
        interactionElement.addEventListener('change', () => {
            handleInteractionChange(setStateUrl, interactionElement, interactionState);
        });
    });
}

// main
createGenreElements(genres);
const interactionElements = getInteractionElements();
const chatElements = getChatElements();
let interactionStates = initInteractionStates(interactionElements);
sessionId = await initilizeBackendConnection(initSession, interactionStates);
if (sessionId) {
    console.log('session id: ', sessionId);
    chatboxListeners(chatBotUrl, null, chatElements, inputIsValid, sessionChatHistory, sessionId);
    interactionListeners(interactionStates, interactionElements);
    displayProducts(products_json);
    pollBackendInteractionStates(getStateUrl, interactionStates, interactionElements, 5000);
}
