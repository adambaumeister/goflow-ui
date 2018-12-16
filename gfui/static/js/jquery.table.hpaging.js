/*
Author 		: Ritesh Gandhi
DOC		    : 10-April-2017
Basic Usage 	: $('#table').hpaging({ "limit": 2 });;
*/

/*
The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
*/

(function ($) {
    $(function () {
        $.widget("blk.hpaging", {
            options: {
                limit: 5,
                activePage: 1,
                parentID: '',
                navBar: null,
                totalPages: ''
            },

            _create: function () {
                var navBar = this._getNavBar();
                $(this.element).after(navBar);
            },

            _getNavBar: function () {
                var nav;
                var elementID = $(this.element).prop("id");
                this.options.parentID = elementID;
                nav = $('<div id=pg_' + elementID + '>').addClass("pagination").data("parentID", elementID);
                this.options.navBar = nav;
                this.setPages(this.options.activePage);
                return nav;
            },

            clearPages: function () {
                $(this.options.navBar).empty();
                $("#" + this.options.parentID + " > tbody > tr").show();
                $("#" + this.options.parentID + " > tbody > tr").removeData("page");
                return true;
            },

            newRow: function (rowNum) {
                this.setPages();
                var rows = $("#" + this.options.parentID + " > tbody > tr");
                var pageNum = $(rows).eq(rowNum).data("page");
                this.activePage(pageNum);
            },

            newLimit: function (pgLimit) {
                this.options.limit = pgLimit;
                if (this.setPages())
                    this.activePage(1);
            },

            setPages: function (pageNum) {
                var retVal = false;
                if (this.clearPages()) {
                    var pageLimit = this.options.limit;
                    var rows = $("#" + this.options.parentID + " > tbody > tr");
                    //var pages = Math.round(rows.length / pageLimit);
                    var pages;
                    var totalPages = rows.length / pageLimit;
                    pages = totalPages;
                    var numArr = totalPages.toString().split(".");
                    if (numArr.length == 2)
                        pages = parseInt(numArr[0]) + 1; 
                    if (pages == 0)
                        pages = 1;
                    var elementID = this.options.parentID;

                    this._setPage(elementID, 1, "<<");
                    this._setPage(elementID, "P-1", "<");
                    var startRow = 0; var endRow = pageLimit;
                    var page;
                    for (var i = 1; i <= pages; i++) {
                        var pgrows;
                        pgrows = rows.slice(startRow, endRow);
                        page = i;
                        $(pgrows).removeData("page");
                        $(pgrows).data("page", page);
                        this._setPage(elementID, page, page);
                        startRow = endRow;
                        endRow = (parseInt(endRow) + parseInt(pageLimit));
                    }
                    this._setPage(elementID, "P+1", ">");
                    this._setPage(elementID, page, ">>");
                    this.options.totalPages = page;
                    if (pageNum !== undefined)
                        this.activePage(pageNum);
                    retVal = true;
                }
                return retVal;
            },

            _setPage: function (parentID, pageNum, pageText) {
                var pageLink = $('<a>', { href: '#', text: (pageText), "data-page": (pageNum) }).appendTo(this.options.navBar);
                this._on(pageLink, {
                    click: "onPageClick"
                });
            },

            activePage: function (pageNum) {
                var num = pageNum * 1;
                this.options.activePage = num;
                $("#" + this.options.parentID + " > tbody > tr").each(function () {
                    if ($(this).data("page") == num) {
                        $(this).show();
                    }
                    else {
                        $(this).hide();
                    }
                });
                this._selectActivePage();
            },

            _selectActivePage: function () {
                var currentPage = this.options.activePage;
                $(this.options.navBar).find("a").each(function () {
                    var linkText = $(this).text();
                    if ($(this).data("page") == currentPage &&
                        (linkText != "<<" && linkText != ">>")) {
                        $(this).attr("class", "active");
                        $(this).siblings().attr("class", "");
                    }
                });
            },

            onPageClick: function (event) {
                event.preventDefault();
                var pageNum = $(event.target).data("page");
                if (pageNum == "P-1") {
                    pageNum = this.options.activePage - 1;
                    if (pageNum < 1)
                        pageNum = 1;
                }
                else if (pageNum == "P+1") {
                    pageNum = this.options.activePage + 1;
                    if (pageNum > this.options.totalPages)
                        pageNum = this.options.totalPages;
                }
                this.activePage(pageNum);
            }
        });
    });
})(jQuery);