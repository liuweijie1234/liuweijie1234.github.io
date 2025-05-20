---
title: CSS 基本用法
date: 2022-12-25 11:42:00
tags:
- CSS
categories:
- Web前端
---


[CSS display（元素显示类型）](http://c.biancheng.net/css3/display.html)

display: none
display 的属性值 none 可以用来隐藏元素，


[css中的hover怎么用](https://www.php.cn/css-tutorial-417948.html)


[css中before的用法是什么](https://www.php.cn/css-tutorial-474802.html)


[css不透明度opacity属性详解](https://www.php.cn/css-tutorial-410372.html)



[css 级联菜单](https://blog.csdn.net/LZGS_4/article/details/46490637)



## CSS 属性



### background 

background 简写属性在一个声明中设置所有的背景属性。

可以设置如下属性：

- background-color
- background-position
- background-size
- background-repeat
- background-origin
- background-clip
- background-attachment
- background-image

| 值 | 描述 |
| -- | -- |
| [background-color](#background-color) | 规定要使用的背景颜色。 |
| background-position | 规定背景图像的位置。 |
| background-size | 规定背景图片的尺寸。 |
| background-repeat | 规定如何重复背景图像。 |
| background-origin | 规定背景图片的定位区域。 |
| background-clip | 规定背景的绘制区域。 |
| background-attachment | 规定背景图像是否固定或者随着页面的其余部分滚动。 |
| background-image | 规定要使用的背景图像。 |
| inherit | 规定应该从父元素继承 background 属性的设置。 |

#### background-color

background-color 属性设置元素的背景颜色。

| 值 | 描述 |
| -- | -- |
| color_name | 规定颜色值为颜色名称的边框颜色（比如 red）。 |
| hex_number | 规定颜色值为十六进制值的边框颜色（比如 #ff0000）。 |
| rgb_number | 规定颜色值为 rgb 代码的边框颜色（比如 rgb(255,0,0)）。 |
| transparent | 默认值。边框颜色为透明。 |
| inherit | 规定应该从父元素继承边框颜色。 |

### box-sizing

box-sizing 属性允许您以特定的方式定义匹配某个区域的特定元素。

例如，假如您需要并排放置两个带边框的框，可通过将 box-sizing 设置为 "border-box"。这可令浏览器呈现出带有指定宽度和高度的框，并把边框和内边距放入框中。

```css
#规定两个并排的带边框的框：

div
{
box-sizing:border-box;
-moz-box-sizing:border-box; /* Firefox */
-webkit-box-sizing:border-box; /* Safari */
width:50%;
float:left;
}
```



### border

border 简写属性在一个声明设置所有的边框属性。

可以按顺序设置如下属性：

- border-width
- border-style（必需）
- border-color

设置 4 个边框的样式：

```css
p
  {
  border:5px solid red;
  }

```

| 值 | 描述 |
| -- | -- |
| border-width | 规定边框的宽度。参阅：[border-width](#border-width) 中可能的值。 |
| border-style | 规定边框的样式。参阅：[border-style](#border-style) 中可能的值。 |
| border-color | 规定边框的颜色。参阅：[border-color](#border-color) 中可能的值。 |
| inherit | 规定应该从父元素继承 border 属性的设置。 |

#### border-radius

border-radius 属性 设置圆角边框

提示：该属性允许您为元素添加圆角边框！

```css
向 div 元素添加圆角边框：

div
{
border:2px solid;
border-radius:25px;
}
```

#### border-width

border-width 简写属性为元素的所有边框设置宽度，或者单独地为各边边框设置宽度。

例子 1
```css
border-width:thin medium thick 10px;
```
上边框是细边框
右边框是中等边框
下边框是粗边框
左边框是 10px 宽的边框

例子 2
```css
border-width:thin medium thick;
```
上边框是 10px
右边框和左边框是中等边框
下边框是粗边框

例子 3
```css
border-width:thin medium;
```
上边框和下边框是细边框
右边框和左边框是中等边框

例子 4
```css
border-width:thin;
```
所有 4 个边框都是细边框

例子 5

设置四个边框的宽度：
```css
p
  {
  border-style:solid;
  border-width:15px;
  }
```
| 值 | 描述 |
| -- | -- |
| thin | 定义细的边框。 |
| medium | 默认。定义中等的边框。 |
| thick | 定义粗的边框。 |
| length | 允许您自定义边框的宽度。 |
| inherit | 规定应该从父元素继承边框宽度。 |


#### border-style

border-style 属性用于设置元素所有边框的样式，或者单独地为各边设置边框样式

```css
border-style:dotted solid double dashed; 
```
上边框是点状
右边框是实线
下边框是双线
左边框是虚线


| 值 | 描述 |
| -- | -- |
| none | 定义无边框。 |
| hidden | 与 "none" 相同。不过应用于表时除外，对于表，hidden 用于解决边框冲突。 |
| dotted | 定义点状边框。在大多数浏览器中呈现为实线。 |
| dashed | 定义虚线。在大多数浏览器中呈现为实线。 |
| solid | 定义实线。 |
| double | 定义双线。双线的宽度等于 border-width 的值。 |
| groove | 定义 3D 凹槽边框。其效果取决于 border-color 的值。 |
| ridge | 定义 3D 垄状边框。其效果取决于 border-color 的值。 |
| inset | 定义 3D inset 边框。其效果取决于 border-color 的值。 |
| outset | 定义 3D outset 边框。其效果取决于 border-color 的值。 |
| inherit | 规定应该从父元素继承边框样式。 |


#### border-color

border-color 属性设置四条边框的颜色。此属性可设置 1 到 4 种颜色。

```css
border-color:red green blue pink;
```
上边框是红色
右边框是绿色
下边框是蓝色
左边框是粉色

| 值 | 描述 |
| -- | -- |
| color_name | 规定颜色值为颜色名称的边框颜色（比如 red）。 |
| hex_number | 规定颜色值为十六进制值的边框颜色（比如 #ff0000）。 |
| rgb_number | 规定颜色值为 rgb 代码的边框颜色（比如 rgb(255,0,0)）。 |
| transparent | 默认值。边框颜色为透明。 |
| inherit | 规定应该从父元素继承边框颜色。 |

### color

color 属性规定文本的颜色。


为不同元素设置文本颜色：
```css
body
  {
  color:red;
  }
h1
  {
  color:#00ff00;
  }
p
  {
  color:rgb(0,0,255);
  }
```

### display

display 属性规定元素应该生成的框的类型。


```css
#使段落生出行内框：

p.inline
  {
  display:inline;
  }
```


| 值 | 描述 |
| -- | -- |
| **none** | 此元素不会被显示,用来隐藏元素。 |
| block | 此元素将显示为块级元素，此元素前后会带有换行符。 |
| inline | 默认。此元素会被显示为内联元素，元素前后没有换行符。 |
| inline-block | 行内块元素。 |
| list-item | 此元素会作为列表显示。 |
| run-in | 此元素会根据上下文作为块级元素或内联元素显示。 |
| table | 此元素会作为块级表格来显示（类似 <table>），表格前后带有换行符。 |
| inline-table | 此元素会作为内联表格来显示（类似 <table>），表格前后没有换行符。 |
| table-row-group | 此元素会作为一个或多个行的分组来显示（类似 <tbody>）。 |
| table-header-group | 此元素会作为一个或多个行的分组来显示（类似 <thead>）。 |
| table-footer-group | 此元素会作为一个或多个行的分组来显示（类似 <tfoot>）。 |
| table-row | 此元素会作为一个表格行显示（类似 <tr>）。 |
| table-column-group | 此元素会作为一个或多个列的分组来显示（类似 <colgroup>）。 |
| table-column | 此元素会作为一个单元格列显示（类似 <col>） |
| table-cell | 此元素会作为一个表格单元格显示（类似 <td> 和 <th>） |
| table-caption | 此元素会作为一个表格标题显示（类似 <caption>） |
| inherit | 规定应该从父元素继承 display 属性的值。 |

### float

float 属性定义元素在哪个方向浮动

把图像向右浮动：
```css
img
  {
  float:right;
  }
```

| 值 | 描述 |
| -- | -- |
| left | 元素向左浮动。 |
| right | 元素向右浮动。 |
| none | 默认值。元素不浮动，并会显示在其在文本中出现的位置。 |
| inherit | 规定应该从父元素继承 float 属性的值。 |

### font

font 简写属性在一个声明中设置所有字体属性。

可以按顺序设置如下属性：

- font-style
- font-variant
- font-weight
- font-size/line-height
- font-family

| 值 | 描述 |
| -- | -- |
| font-style | 规定字体样式。参阅：[font-style](#font-style) 中可能的值。 |
| font-variant | 规定字体异体。参阅：[font-variant](#font-variant) 中可能的值。 |
| font-weight | 规定字体粗细。参阅：[font-weight](#font-weight) 中可能的值。 |
| font-size/line-height | 规定字体尺寸和行高。参阅：[font-size](#font-size) 和 [line-height](#line-height) 中可能的值。 |
| font-family | 规定字体系列。参阅：[font-family](#font-family) 中可能的值。 |
| caption | 定义被标题控件（比如按钮、下拉列表等）使用的字体。 |
| icon | 定义被图标标记使用的字体。 |
| menu | 定义被下拉列表使用的字体。 |
| message-box | 定义被对话框使用的字体。 |
| small-caption | caption 字体的小型版本。 |
| status-bar | 定义被窗口状态栏使用的字体。 |

#### font-style

font-style 属性定义字体的风格。

#### font-variant

font-variant 属性设置小型大写字母的字体显示文本，这意味着所有的小写字母均会被转换为大写，但是所有使用小型大写字体的字母与其余文本相比，其字体尺寸更小。

#### font-weight

font-weight 属性设置文本的粗细。

| 值 | 描述 |
| -- | -- |
| normal | 默认值。定义标准的字符。 |
| bold | 定义粗体字符。 |
| bolder | 定义更粗的字符。 |
| lighter | 定义更细的字符。 |
| 100-900 | 定义由粗到细的字符。400 等同于 normal，而 700 等同于 bold。 |
| inherit | 规定应该从父元素继承字体的粗细。 |


#### font-size

font-size 属性可设置字体的尺寸。

| 值 | 描述 |
| -- | -- |
| xx-small<br>x-small<br>small<br>medium<br>large<br>x-large<br>xx-large | 把字体的尺寸设置为不同的尺寸，从 xx-small 到 xx-large。<br>默认值：medium。 |
| smaller | 把 font-size 设置为比父元素更小的尺寸。 |
| larger | 把 font-size 设置为比父元素更大的尺寸。 |
| length | 把 font-size 设置为一个固定的值。 |
| % | 把 font-size 设置为基于父元素的一个百分比值。 |
| inherit | 规定应该从父元素继承字体尺寸。 |

#### font-family

font-family 规定元素的字体系列。


### height

width 属性设置元素的宽度。
height 属性设置元素的高度。

设置段落的高度和宽度：
```css
p
  {
  height:100px;
  width:100px;
  }
```

#### line-height

line-height 属性设置行间的距离（行高）。

注释：不允许使用负值。

### margin

margin 简写属性在一个声明中设置所有外边距属性。该属性可以有 1 到 4 个值。

```css
margin:10px 5px 15px 20px;
```
上外边距是 10px
右外边距是 5px
下外边距是 15px
左外边距是 20px

#### margin-top

margin-top 属性设置元素的上外边距。


设置 p 元素的上外边距：
```css
p
  {
  margin-top:2cm;
  }
```

#### margin-bottom

margin-bottom 属性设置元素的下外边距。

#### margin-left

margin-left 属性设置元素的左外边距。

#### margin-right

margin-right 属性设置元素的右外边距。

### max-width

max-width 定义元素的最大宽度。

```css
#设置段落的最大宽度：
p
  {
  max-width:100px;
  }
```

### overflow

overflow 属性规定当内容溢出元素框时发生的事情。


设置 overflow 属性：
```css
div
  {
  width:150px;
  height:150px;
  overflow:scroll;
  }
```

| 值 | 描述 |
| -- | -- |
| visible | 默认值。内容不会被修剪，会呈现在元素框之外。 |
| hidden | 内容会被修剪，并且其余内容是不可见的。 |
| scroll | 内容会被修剪，但是浏览器会显示滚动条以便查看其余的内容。 |
| auto | 如果内容被修剪，则浏览器会显示滚动条以便查看其余的内容。 |
| inherit | 规定应该从父元素继承 overflow 属性的值。 |

#### overflow-x 


overflow-x 属性规定是否对内容的左/右边缘进行裁剪 - 如果溢出元素内容区域的话。

裁剪 div 元素中内容的左/右边缘 - 如果溢出元素的内容区域的话：
```css
div
{
overflow-x:hidden;
}
```

| 值 | 描述 |
| -- | -- |
| visible | 不裁剪内容，可能会显示在内容框之外。 |
| hidden | 裁剪内容 - 不提供滚动机制。 |
| scroll | 裁剪内容 - 提供滚动机制。 |
| auto | 如果溢出框，则应该提供滚动机制。 |
| no-display | 如果内容不适合内容框，则删除整个框。 |
| no-content | 如果内容不适合内容框，则隐藏整个内容。 |


#### overflow-y


overflow-y 属性规定是否对内容的上/下边缘进行裁剪 - 如果溢出元素内容区域的话。


裁剪 div 元素中内容的左/右边缘 - 如果溢出元素的内容区域的话：
```css
div
{
overflow-y:hidden;
}
```

| 值 | 描述 |
| -- | -- |
| visible | 不裁剪内容，可能会显示在内容框之外。 |
| hidden | 裁剪内容 - 不提供滚动机制。 |
| scroll | 裁剪内容 - 提供滚动机制。 |
| auto | 如果溢出框，则应该提供滚动机制。 |
| no-display | 如果内容不适合内容框，则删除整个框。 |
| no-content | 如果内容不适合内容框，则隐藏整个内容。 |


### padding

padding 简写属性在一个声明中设置所有内边距属性。


例子 1
```css
padding:10px 5px 15px 20px;
```
上内边距是 10px
右内边距是 5px
下内边距是 15px
左内边距是 20px

例子 2
```css
padding:10px 5px 15px;
```
上内边距是 10px
右内边距和左内边距是 5px
下内边距是 15px

例子 3
```css
padding:10px 5px;
```
上内边距和下内边距是 10px
右内边距和左内边距是 5px

例子 4
```css
padding:10px;
```
所有 4 个内边距都是 10px



### width

width 属性设置元素的宽度。

说明:

这个属性定义元素内容区的宽度，在内容区外面可以增加内边距、边框和外边距。

行内非替换元素会忽略这个属性。


设置段落的高度和宽度：
```css
p
  {
  height:100px;
  width:100px;
  }
```

| 值 | 描述 |
| -- | -- |
| auto | 默认值。浏览器可计算出实际的宽度。 |
| length | 使用 px、cm 等单位定义宽度。 |
| % | 定义基于包含块（父元素）宽度的百分比宽度。 |
| inherit | 规定应该从父元素继承 width 属性的值。 |