from ebooklib import epub



from src.chapters import ChapterRequester


class TextConverter:
    def __init__(self, title, begin, end):

        self.title  = title
        self.begin  = begin
        self.end  = end
       
        self.book = epub.EpubBook()
        self.initialize_book()
        self.save_book()

    def initialize_book(self):
        self.book.set_identifier('id{begin}{end}'.format(begin = self.begin, end=self.end))
        self.book.set_title(self.title)
        self.book.set_language('en')


    def save_book(self):
        self.chapters_list = list(range(self.begin, self.end + 1))
        print("Compiling book")
        for chapt in self.chapters_list:
     
            c = ChapterRequester(title=self.title, number=chapt)
      
            c1 = epub.EpubHtml(title=str(chapt), file_name='chap_{id}.xhtml'.format(id=chapt), lang='hr')
            c1.content=u'<h1>{heading}</h1><p>{text}</p>'.format( heading=c.chapter.title, text=c.chapter.text_content)
            self.book.add_item(c1)
            self.book.spine.extend((c1,))
            self.book.toc.extend((c1,))
           
        
        style = 'BODY {color: white;}'
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

        self.book.add_item(nav_css)

        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())


        
       

        epub.write_epub('{title}.epub'.format(title = self.title), self.book, {})


    def convert_epub(self):
        self.book.set_identifier('id123456')
        self.book.set_title(self.title)
        self.book.set_language('en')
        #self.book.add_author(self.author)

        self.c1 = epub.EpubHtml(title=self.title, file_name='chap_01.xhtml', lang='hr')
        self.c1.content=u'<h1>Intro heading</h1><p>{text}</p>'.format(text=self.text)
        self.book.add_item(self.c1)

        self.book.toc = (epub.Link('chap_01.xhtml', 'Introduction', 'intro'),
             (epub.Section('Simple book'),
             (self.c1, ))
            )

        self.book.add_item(epub.EpubNcx())
        self.book.add_item(epub.EpubNav())

        style = 'BODY {color: white;}'
        nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

        self.book.add_item(nav_css)

        self.book.spine = ['nav', self.c1]
        
        epub.write_epub('test.epub', self.book, {})

    def multithreaded_save(self):
        print('Processing with threads...')

        self.num_list = list(range(self.number - self.go_back,self.number))
       
        def read_data(num):
            c = ChapterRequester(
            number=num, site=self.site, title=self.title)

            self.collected_text.append(c.chapter.text_content)

        threadpool = Threadpool(processes = self.NUM_THREADS)
        self.collected_text = []

        results = threadpool.map(read_data, self.num_list)

        #print(self.collected_text)

        self.collected_text = " ".join(self.collected_text)

        return self






