USE [SEU_BD]
GO

/****** Object:  Table [dbo].[CTe]    Script Date: 06/11/2023 16:43:35 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[CTe](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[chCTe] [varchar](44) NOT NULL,
	[dhEmi] [smalldatetime] NULL,
	[dProg] [date] NULL,
	[nCT] [int] NOT NULL,
	[tpCTe] [int] NULL,
	[tpServ] [int] NULL,
	[tpEmis] [int] NULL,
	[cMunIni] [int] NULL,
	[xMunIni] [nvarchar](255) NULL,
	[UFIni] [char](2) NULL,
	[cMunFim] [int] NULL,
	[xMunFim] [nvarchar](255) NULL,
	[UFFim] [char](2) NULL,
	[vTPrest] [decimal](10, 2) NULL,
	[vCarga] [decimal](10, 2) NULL,
	[chaveNF] [varchar](44) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO;


USE [SEU_BD]
GO

/****** Object:  Table [dbo].[CTeCancelamento]    Script Date: 06/11/2023 16:44:24 ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[CTeCancelamento](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[chCTe] [varchar](44) NOT NULL,
	[tpEvento] [varchar](10) NULL,
	[xEvento] [varchar](25) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

