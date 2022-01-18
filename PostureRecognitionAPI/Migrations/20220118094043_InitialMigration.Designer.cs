﻿// <auto-generated />
using System;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Infrastructure;
using Microsoft.EntityFrameworkCore.Migrations;
using Microsoft.EntityFrameworkCore.Storage.ValueConversion;
using Npgsql.EntityFrameworkCore.PostgreSQL.Metadata;
using PostureRecognitionAPI.Data;

namespace PostureRecognitionAPI.Migrations
{
    [DbContext(typeof(DataContext))]
    [Migration("20220118094043_InitialMigration")]
    partial class InitialMigration
    {
        protected override void BuildTargetModel(ModelBuilder modelBuilder)
        {
#pragma warning disable 612, 618
            modelBuilder
                .HasAnnotation("Relational:MaxIdentifierLength", 63)
                .HasAnnotation("ProductVersion", "5.0.5")
                .HasAnnotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn);

            modelBuilder.Entity("PostureRecognitionAPI.Models.DangerZoneCoordinates", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("integer")
                        .HasAnnotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn);

                    b.Property<int>("CameraId")
                        .HasColumnType("integer");

                    b.Property<string>("Coordinates")
                        .HasColumnType("text");

                    b.HasKey("Id");

                    b.ToTable("DangerZoneCoordinates");
                });

            modelBuilder.Entity("PostureRecognitionAPI.Models.PostureLog", b =>
                {
                    b.Property<int>("Id")
                        .ValueGeneratedOnAdd()
                        .HasColumnType("integer")
                        .HasAnnotation("Npgsql:ValueGenerationStrategy", NpgsqlValueGenerationStrategy.IdentityByDefaultColumn);

                    b.Property<int>("CameraId")
                        .HasColumnType("integer");

                    b.Property<string>("Classification")
                        .HasColumnType("text");

                    b.Property<DateTime>("DateTime")
                        .HasColumnType("timestamp without time zone");

                    b.Property<string>("PostureLandmarks")
                        .HasColumnType("text");

                    b.Property<string>("Zone")
                        .HasColumnType("text");

                    b.HasKey("Id");

                    b.ToTable("PostureLogs");
                });
#pragma warning restore 612, 618
        }
    }
}
