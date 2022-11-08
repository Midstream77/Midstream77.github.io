from blog_func import blog_func


class blog_gen(blog_func):
    """generate a html file for blog page"""

    def gen_template(self):
        """generate the content of the blogpage html file"""

        # read the conent in the input.txt and transfer all the space and tab into '&ensp;'
        f = open("./input.txt", "r", encoding="utf-8")
        text = f.read()
        text_list = list(text)
        for i in range(len(text)):
            if text_list[i] == " ":
                text_list[i] = "&ensp;"
            if text_list[i] == "\t":
                text_list[i] = "&ensp;&ensp;&ensp;&ensp;"

        # split the text by paragraphs
        text = "".join(text_list).split("\n")

        # add '<article>' '</article>' tag to each line to make sure each paragraph is a seperated.
        for i in range(len(text)):
            text[i] = "<article>\n" + text[i] + "\n</article>\n"
        text = "".join(text)

        # generate html piece for tags
        tags_text = ''
        for i in range(len(self.tags)):
            tags_text += '<a href="{tag_link}" class = "blog_tag">#{tag_name}</a>\n'.format(
                tag_link='../html/'+self.tags[i]+'.html',
                tag_name=self.tags[i])

        # generate and return the content of the blog html
        template = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Midstreamblog</title>

    <link rel="stylesheet" href="../css/reset.css">
    <link rel="stylesheet" href="../css/main.css">
    <link rel="stylesheet" href="../font/iconfont.css">
    <script type="text/javascript" src="../js/tools.js"></script>

</head>

<body>
    <div class="cover_left">
        <div class="cover_last_left">
            <img src="../img/logo.jpg" id="logo">
            <h2>Midstream Blog</h2>
            <div class="cover_last_left_divider"></div>
            <h4>just the place about me</h4>
        </div>

        <div class="nav_panel_list_icon_hidden"><a class="list_icon" href="javascript:void(0)"
                onclick="list_icon_click()"><span class="iconfont">&#xe7be;</a></div>

        <div class="cover_panel">
            <div class="nav_panel">
                <div class="nav_panel_element"><a class="nav_panel_element_link" href="../html/tags.html"><span
                            class="iconfont">&#xe7b6;<div class="icon_dis">标签</div></span></a></div>
                <div class="nav_panel_element"><a class="nav_panel_element_link" href="../html/friends.html"><span
                            class="iconfont">&#xe61d;<div class="icon_dis">友链</div></span></a></div>
                <div class="nav_panel_element"><a class="nav_panel_element_link" href="../html/about.html"><span
                            class="iconfont">&#xe7b7;<div class="icon_dis">关于</div></span></a></div>
                <div class="nav_panel_element_hidden"><a class="nav_panel_element_link" href="../index.html"><span
                            class="iconfont">&#xe7bf;<div class="icon_dis">主页</div></span></a></div>
            </div>

            <a href="../index.html"><button id="btn_home">home</button></a>
        </div>
    </div>

    <div class="content_right">
        <h2 class="blog_title">{title}</h2>
        <p class="blog_date">{date}</p>

        <div class="blog_content_block">
            {article}
        </div>

        <div class="blog_tag_block">
            {tags}
        </div>
        
        <div class="block_divider_long"></div>
    </div>


</body>



<script src="../js/window.js"></script>
<script>
    window.onload = resize();
</script>

<script type="text/javascript" src="../js/window.js"></script>

</html>
        """.format(
            title=self.title,
            date=self.post_time,
            article=text,
            tags=tags_text,
        )
        f.close()

        # to make the template be able to contain the empty line
        key = 0
        keywords = "<article>\n\n</article>"
        while key != -1:
            key = template.find(keywords)
            if key != -1:
                template = (
                    template[:key]
                    + "<article>\n&ensp;\n</article>"
                    + template[key + len(keywords):]
                )
        return template

    def gen_html(self):
        """generate the blogpage html file in the right folder"""

        # generate the path of the html file
        fname = self.blog_path + "/" + self.title + ".html"

        # avoid wrong submittion to cover the older blogs
        blog = self.Path(fname)
        if blog.exists():
            print("blog existed")
            raise IndexError

        # generate the html file and write the content in it
        else:
            f = open(fname, "w", encoding="utf-8")
            template = self.gen_template()
            f.write(template)
            f.close()