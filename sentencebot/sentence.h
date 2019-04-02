#ifndef SENTENCE_H
#define SENTENCE_H

const char * NOUNS[] = {
    "time", "year", "people", "way", "day", "man", "thing", "woman", "life",
    "child", "world", "school", "state", "family", "student", "group", "country",
    "problem", "hand", "part", "place", "case", "week", "company", "system",
    "program", "question", "work", "government", "number", "night", "point",
    "home", "water", "room", "mother", "area", "money", "story", "fact", "month",
    "lot", "right", "study", "book", "eye", "job", "word", "business", "issue",
    "side", "kind", "head", "house", "service", "friend", "father", "power",
    "hour", "game", "line", "end", "member", "law", "car", "city", "community",
    "name", "president", "team", "minute", "idea", "kid", "body", "information",
    "back", "parent", "face", "others", "level", "office", "door", "health",
    "person", "art", "war", "history", "party", "result", "change", "morning",
    "reason", "research", "girl", "guy", "moment", "air", "teacher", "force",
    "education", "flag"
};

const char * PROPER_NOUNS[] = {
    "George Washington", "John Adams", "Thomas Jefferson", "James Madison", "James Monroe",
    "John Quincy Adams", "Andrew Jackson", "Martin Van Buren", "William Henry Harrison", "John Tyler",
    "James K. Polk", "Zachary Taylor",  "Millard Fillmore", "Franklin Pierce", "James Buchanan",
    "Abraham Lincoln", "Andrew Johnson", "Ulysses S. Grant", "Rutherford B. Hayes", "James A. Garfield",
    "Chester Arthur", "Grover Cleveland", "Benjamin Harrison", "Grover Cleveland", "William McKinley",
    "Theodore Roosevelt", "William Howard Taft", "Woodrow Wilson", "Warren G. Harding", "Calvin Coolidge",
    "Herbert Hoover", "Franklin D. Roosevelt", "Harry S. Truman", "Dwight D. Eisenhower", "John F. Kennedy",
    "Lyndon B. Johnson", "Richard Nixon", "Gerald Ford", "Jimmy Carter", "Ronald Reagan", "George Bush",
    "Bill Clinton", "George W. Bush", "Barack Obama", "Donald Trump"
};

const char * VERBS[] = {
    "be", "have", "do", "say", "go", "can", "get", "would",
    "make", "know", "will", "think", "take", "see", "come", "could",
    "want", "look", "use", "find", "give", "tell", "work", "may", "should",
    "call", "try", "ask", "need", "feel", "become", "leave","put", "mean",
    "keep", "let", "begin", "seem", "help", "talk", "turn", "start",
    "might", "show", "hear", "play", "run", "move", "like", "live", "believe",
    "hold", "bring", "happen", "must", "write", "provide", "sit", "stand",
    "lose", "pay", "meet", "include", "continue", "set", "learn", "change",
    "lead", "understand", "watch", "follow", "stop", "create", "speak", "read",
    "allow", "add", "spend", "grow", "open", "walk", "win", "offer", "remember", "love",
    "consider", "appear", "buy", "wait", "serve", "die", "send", "expect", "build",
    "stay", "fall", "cut", "reach", "kill", "remain", "is"
};

const char * ARTICLES[] = {"a", "some", "many", "few", "most", "the"};

const char* PREPOSITIONS[] =  {"to", "from", "over", "under", "on", "beside", "around"};

// sizeof(NOUNS) will tell me the size of the NOUNS array in bytes.
// Since it's an array of pointers it's going to be (8 * number_of_nouns)
// on a 64 bit system and (4 * number_of_nouns) on a 32 bit system.
// Need to divide by the size of an entry (either 8 or 4) to get the number
// of entries.
const int NOUNS_SIZE = sizeof(NOUNS)/sizeof(NOUNS[0]);
const int VERBS_SIZE = sizeof(VERBS)/sizeof(VERBS[0]);
const int ARTICLES_SIZE = sizeof(ARTICLES)/sizeof(ARTICLES[0]);
const int PREPOSITIONS_SIZE = sizeof(PREPOSITIONS)/sizeof(PREPOSITIONS[0]);
const int PROPER_NOUNS_SIZE = sizeof(PROPER_NOUNS)/sizeof(PROPER_NOUNS[0]);

#endif