"""
Popular Books Database

A curated collection of popular, impactful books across various genres.
Perfect for generating book summaries.
"""

POPULAR_BOOKS = [
    # Self-Help & Personal Development
    {
        "title": "Atomic Habits",
        "author": "James Clear",
        "genre": "self-help",
        "year": 2018,
        "description": "Tiny changes, remarkable results"
    },
    {
        "title": "The 7 Habits of Highly Effective People",
        "author": "Stephen Covey",
        "genre": "self-help",
        "year": 1989,
        "description": "Powerful lessons in personal change"
    },
    {
        "title": "Deep Work",
        "author": "Cal Newport",
        "genre": "productivity",
        "year": 2016,
        "description": "Rules for focused success in a distracted world"
    },
    {
        "title": "The Power of Now",
        "author": "Eckhart Tolle",
        "genre": "spirituality",
        "year": 1997,
        "description": "A guide to spiritual enlightenment"
    },
    {
        "title": "How to Win Friends and Influence People",
        "author": "Dale Carnegie",
        "genre": "self-help",
        "year": 1936,
        "description": "The classic guide to better relationships"
    },
    {
        "title": "The Subtle Art of Not Giving a F*ck",
        "author": "Mark Manson",
        "genre": "self-help",
        "year": 2016,
        "description": "A counterintuitive approach to living a good life"
    },
    {
        "title": "Think and Grow Rich",
        "author": "Napoleon Hill",
        "genre": "self-help",
        "year": 1937,
        "description": "The classic wealth-building guide"
    },
    {
        "title": "The Four Agreements",
        "author": "Don Miguel Ruiz",
        "genre": "spirituality",
        "year": 1997,
        "description": "A practical guide to personal freedom"
    },
    
    # Business & Leadership
    {
        "title": "Good to Great",
        "author": "Jim Collins",
        "genre": "business",
        "year": 2001,
        "description": "Why some companies make the leap and others don't"
    },
    {
        "title": "The Lean Startup",
        "author": "Eric Ries",
        "genre": "business",
        "year": 2011,
        "description": "How constant innovation creates radically successful businesses"
    },
    {
        "title": "Start with Why",
        "author": "Simon Sinek",
        "genre": "business",
        "year": 2009,
        "description": "How great leaders inspire everyone to take action"
    },
    {
        "title": "Zero to One",
        "author": "Peter Thiel",
        "genre": "business",
        "year": 2014,
        "description": "Notes on startups, or how to build the future"
    },
    {
        "title": "The Hard Thing About Hard Things",
        "author": "Ben Horowitz",
        "genre": "business",
        "year": 2014,
        "description": "Building a business when there are no easy answers"
    },
    {
        "title": "Principles",
        "author": "Ray Dalio",
        "genre": "business",
        "year": 2017,
        "description": "Life and work principles from a legendary investor"
    },
    
    # Psychology & Behavior
    {
        "title": "Thinking, Fast and Slow",
        "author": "Daniel Kahneman",
        "genre": "psychology",
        "year": 2011,
        "description": "How two systems drive the way we think"
    },
    {
        "title": "Influence: The Psychology of Persuasion",
        "author": "Robert Cialdini",
        "genre": "psychology",
        "year": 1984,
        "description": "The psychology behind why people say yes"
    },
    {
        "title": "Predictably Irrational",
        "author": "Dan Ariely",
        "genre": "psychology",
        "year": 2008,
        "description": "The hidden forces that shape our decisions"
    },
    {
        "title": "The Psychology of Money",
        "author": "Morgan Housel",
        "genre": "finance",
        "year": 2020,
        "description": "Timeless lessons on wealth, greed, and happiness"
    },
    {
        "title": "Mindset: The New Psychology of Success",
        "author": "Carol Dweck",
        "genre": "psychology",
        "year": 2006,
        "description": "How we can learn to fulfill our potential"
    },
    
    # Philosophy & Wisdom
    {
        "title": "Meditations",
        "author": "Marcus Aurelius",
        "genre": "philosophy",
        "year": 180,
        "description": "Stoic wisdom from a Roman emperor"
    },
    {
        "title": "Man's Search for Meaning",
        "author": "Viktor Frankl",
        "genre": "philosophy",
        "year": 1946,
        "description": "Finding purpose in suffering"
    },
    {
        "title": "The Almanack of Naval Ravikant",
        "author": "Eric Jorgenson",
        "genre": "philosophy",
        "year": 2020,
        "description": "A guide to wealth and happiness"
    },
    {
        "title": "Letters from a Stoic",
        "author": "Seneca",
        "genre": "philosophy",
        "year": 65,
        "description": "Practical philosophy for modern life"
    },
    
    # Science & Technology
    {
        "title": "Sapiens: A Brief History of Humankind",
        "author": "Yuval Noah Harari",
        "genre": "science",
        "year": 2011,
        "description": "The story of how we became who we are"
    },
    {
        "title": "A Brief History of Time",
        "author": "Stephen Hawking",
        "genre": "science",
        "year": 1988,
        "description": "From the Big Bang to black holes"
    },
    {
        "title": "The Gene: An Intimate History",
        "author": "Siddhartha Mukherjee",
        "genre": "science",
        "year": 2016,
        "description": "The story of the gene and its impact on human lives"
    },
    
    # Biographies & Memoirs
    {
        "title": "Steve Jobs",
        "author": "Walter Isaacson",
        "genre": "biography",
        "year": 2011,
        "description": "The life of Apple's visionary founder"
    },
    {
        "title": "Shoe Dog",
        "author": "Phil Knight",
        "genre": "biography",
        "year": 2016,
        "description": "A memoir by the creator of Nike"
    },
    {
        "title": "The Autobiography of Benjamin Franklin",
        "author": "Benjamin Franklin",
        "genre": "biography",
        "year": 1791,
        "description": "The life of a founding father"
    },
    {
        "title": "Elon Musk",
        "author": "Walter Isaacson",
        "genre": "biography",
        "year": 2023,
        "description": "The definitive biography of the world's most controversial innovator"
    },
    
    # Health & Wellness
    {
        "title": "Why We Sleep",
        "author": "Matthew Walker",
        "genre": "health",
        "year": 2017,
        "description": "Unlocking the power of sleep and dreams"
    },
    {
        "title": "The Body Keeps the Score",
        "author": "Bessel van der Kolk",
        "genre": "health",
        "year": 2014,
        "description": "Brain, mind, and body in the healing of trauma"
    },
    {
        "title": "Breath",
        "author": "James Nestor",
        "genre": "health",
        "year": 2020,
        "description": "The new science of a lost art"
    },
    
    # Finance & Investing
    {
        "title": "Rich Dad Poor Dad",
        "author": "Robert Kiyosaki",
        "genre": "finance",
        "year": 1997,
        "description": "What the rich teach their kids about money"
    },
    {
        "title": "The Intelligent Investor",
        "author": "Benjamin Graham",
        "genre": "finance",
        "year": 1949,
        "description": "The definitive book on value investing"
    },
    {
        "title": "A Random Walk Down Wall Street",
        "author": "Burton Malkiel",
        "genre": "finance",
        "year": 1973,
        "description": "The time-tested strategy for successful investing"
    },
    
    # Creativity & Innovation
    {
        "title": "Steal Like an Artist",
        "author": "Austin Kleon",
        "genre": "creativity",
        "year": 2012,
        "description": "10 things nobody told you about being creative"
    },
    {
        "title": "The War of Art",
        "author": "Steven Pressfield",
        "genre": "creativity",
        "year": 2002,
        "description": "Break through the blocks and win your inner creative battles"
    },
    {
        "title": "Big Magic",
        "author": "Elizabeth Gilbert",
        "genre": "creativity",
        "year": 2015,
        "description": "Creative living beyond fear"
    },
    
    # Communication & Relationships
    {
        "title": "Never Split the Difference",
        "author": "Chris Voss",
        "genre": "business",
        "year": 2016,
        "description": "Negotiating as if your life depended on it"
    },
    {
        "title": "Crucial Conversations",
        "author": "Kerry Patterson",
        "genre": "communication",
        "year": 2002,
        "description": "Tools for talking when stakes are high"
    },
    {
        "title": "The 5 Love Languages",
        "author": "Gary Chapman",
        "genre": "relationships",
        "year": 1992,
        "description": "The secret to love that lasts"
    },
]


def get_book_by_title(title: str) -> dict | None:
    """Find a book by its title (case-insensitive)."""
    title_lower = title.lower()
    for book in POPULAR_BOOKS:
        if book["title"].lower() == title_lower:
            return book
    return None


def get_books_by_genre(genre: str) -> list:
    """Get all books of a specific genre."""
    genre_lower = genre.lower()
    return [book for book in POPULAR_BOOKS if book.get("genre", "").lower() == genre_lower]


def search_books(query: str) -> list:
    """Search books by title or author."""
    query_lower = query.lower()
    results = []
    for book in POPULAR_BOOKS:
        if query_lower in book["title"].lower() or query_lower in book["author"].lower():
            results.append(book)
    return results

